/** @file
  This file contains routines that support PCI Express initialization

  Copyright (c) 2024, Intel Corporation. All rights reserved.<BR>
  SPDX-License-Identifier: BSD-2-Clause-Patent
**/
#include <Uefi/UefiBaseType.h>
#include <IndustryStandard/Pci.h>
#include <Library/BaseMemoryLib.h>
#include <Library/PcieHelperLib.h>
#include <Library/PchSbiAccessLib.h>
#include <Library/PchPciBdfLib.h>
#include <Library/PcieRpLib.h>
#include <Library/PchInfoLib.h>
#include <Register/PchPcieRpRegs.h>
#include <Register/PcieSipRegs.h>
#include <PcieRegs.h>
#include <CpuPcieInfo.h>

/**
  Get PCIe port number for enabled port.
  @param[in] RpBase    Root Port pci segment base address

  @retval Root Port number (1 based)
**/
UINT32
EFIAPI
PciePortNum (
  IN     UINT64  RpBase
  )
{
  return PciSegmentRead32 (RpBase + R_PCIE_CFG_LCAP) >> N_PCIE_CFG_LCAP_PN;
}

/**
  Get PCIe root port index

  @param[in] RpBase    Root Port pci segment base address

  @retval Root Port index (0 based)
**/
UINT32
EFIAPI
PciePortIndex (
  IN     UINT64  RpBase
  )
{
  return PciePortNum (RpBase) - 1;
}

/**
  This function checks whether PHY lane power gating is enabled on the port.

  @param[in] RpBase                 Root Port base address

  @retval TRUE                      PHY power gating is enabled
  @retval FALSE                     PHY power gating disabled
**/
BOOLEAN
EFIAPI
PcieIsPhyLanePgEnabled (
  IN     UINT64  RpBase
  )
{
  UINT32 Data32;

  Data32 = PciSegmentRead32 (RpBase + R_PCH_PCIE_CFG_PCIEPMECTL);
  return (Data32 & B_PCH_PCIE_CFG_PCIEPMECTL_DLSULPPGE) != 0;
}

/**
  Configures LTR override in Root Port's proprietary registers.

  @param[in] Segment,Bus,Device,Function    address of currently visited PCIe device
  @param[in] DevNum                         currently visited device number
  @param[in] TreeLtr                        combination of LTR override values from all devices under this Root Port
  @param[in] LtrConfig                      Root Port LTR configuration
**/
VOID
EFIAPI
ConfigureRpLtrOverride (
  UINT64           RpBase,
  UINT32           DevNum,
  LTR_OVERRIDE     *TreeLtr,
  PCIE_LTR_CONFIG  *LtrConfig
  )
{
  UINT32       OvrEn;
  UINT32       OvrVal;
  BOOLEAN      IsCpuPcie;
  UINT32       LtrCfgLock;

  IsCpuPcie = FALSE;
  OvrEn = 0;
  OvrVal = 0;
  LtrCfgLock = 0;

  if (DevNum == SA_PEG0_DEV_NUM || DevNum == SA_PEG3_DEV_NUM) {
    IsCpuPcie = TRUE;
  }

  //
  // LTR settings from LTROVR register only get acknowledged on rising edge of LTROVR2[1:0]
  // If those bits were already set (that can happen on a plug-hotUnplug-hotPlug scenario),
  // they need to be toggled
  //
  if (PciSegmentRead32 (RpBase + R_PCH_PCIE_CFG_LTROVR2) != 0) {
    PciSegmentWrite32 (RpBase + R_PCH_PCIE_CFG_LTROVR2, 0);
  }
  //
  // (*)LatencyOverrideMode = 0 -> no override
  //                          1 -> override with RP policy values
  //                          2 -> override with endpoint's override values
  //

  if (LtrConfig->ForceLtrOverride || TreeLtr->ForceOverride) {
    OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_FORCE_OVERRIDE;
  }
  if (LtrConfig->LtrConfigLock == TRUE) {
    OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_LOCK;
    if (IsCpuPcie) {
      LtrCfgLock |= (UINT32) B_PCIE_CFG_LPCR_LTRCFGLOCK;
    }
  }

  if (LtrConfig->SnoopLatencyOverrideMode == 1) {
    OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_LTRSOVREN;
    OvrVal |= LtrConfig->SnoopLatencyOverrideValue;
    OvrVal |= LtrConfig->SnoopLatencyOverrideMultiplier << 10;
    OvrVal |= (UINT32) B_PCH_PCIE_CFG_LTROVR_LTRSROVR;
  } else if (LtrConfig->SnoopLatencyOverrideMode == 2) {
    if (TreeLtr->MaxSnoopLatencyRequirement) {
      OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_LTRSOVREN;
      OvrVal |= TreeLtr->MaxSnoopLatencyValue;
      OvrVal |= TreeLtr->MaxSnoopLatencyScale << 10;
      OvrVal |= (UINT32) B_PCH_PCIE_CFG_LTROVR_LTRSROVR;
    }
  }
  if (LtrConfig->NonSnoopLatencyOverrideMode == 1) {
    OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_LTRNSOVREN;
    OvrVal |= LtrConfig->NonSnoopLatencyOverrideValue << 16;
    OvrVal |= LtrConfig->NonSnoopLatencyOverrideMultiplier << 26;
    OvrVal |= (UINT32) B_PCH_PCIE_CFG_LTROVR_LTRNSROVR;
  } else if (LtrConfig->NonSnoopLatencyOverrideMode == 2) {
    if (TreeLtr->MaxNoSnoopLatencyRequirement) {
      OvrEn |= (UINT32) B_PCH_PCIE_CFG_LTROVR2_LTRNSOVREN;
      OvrVal |= TreeLtr->MaxNoSnoopLatencyValue << 16;
      OvrVal |= TreeLtr->MaxNoSnoopLatencyScale << 26;
      OvrVal |= (UINT32) B_PCH_PCIE_CFG_LTROVR_LTRNSROVR;
    }
  }
  PciSegmentWrite32 (RpBase + R_PCH_PCIE_CFG_LTROVR, OvrVal);
  PciSegmentWrite32 (RpBase + R_PCH_PCIE_CFG_LTROVR2, OvrEn);
  if (IsCpuPcie) {
    PciSegmentOr32(RpBase + R_PCIE_CFG_LPCR, LtrCfgLock);
  }
  DEBUG ((DEBUG_INFO, "ConfigureRpLtrOverride %x Val %x En %x\n", RpBase, OvrVal, OvrEn));
}

/**
  Configures proprietary parts of L1 substates configuration in Root Port

  @param[in] RpBase       Root Port pci segment base address
  @param[in] LtrCapable   TRUE if Root Port is LTR capable
  @param[in] L1LowCapable   TRUE if Root Port is L1 Low capable
**/
VOID
EFIAPI
L1ssProprietaryConfiguration (
  UINT64  RpBase,
  BOOLEAN LtrCapable,
  BOOLEAN L1LowCapable
  )
{
  BOOLEAN ClkreqSupported;
  BOOLEAN L1ssEnabled;
  UINT16  PcieCapOffset;
  UINT32  Data32;
  BOOLEAN L1LowSupported;

  ClkreqSupported = PcieIsPhyLanePgEnabled (RpBase);

  PcieCapOffset = PcieBaseFindExtendedCapId (RpBase, V_PCIE_EX_L1S_CID);
  if (PcieCapOffset == 0) {
    L1ssEnabled = FALSE;
  } else {
    Data32 = PciSegmentRead32 (RpBase + PcieCapOffset + R_PCIE_EX_L1SCTL1_OFFSET);
    L1ssEnabled = Data32 & (B_PCIE_EX_L1SCAP_AL1SS | B_PCIE_EX_L1SCAP_AL12S | B_PCIE_EX_L1SCAP_PPL11S |B_PCIE_EX_L1SCAP_PPL12S);
  }
  L1LowSupported = ClkreqSupported && LtrCapable && !L1ssEnabled && L1LowCapable;

  ///
  /// If L1.SNOOZ and L1.OFF (L1 Sub-States) are not supported and per-port CLKREQ# is supported, and LTR is supported:
  /// Enable L1.LOW by setting Dxx:Fn:420[17] = 1b
  ///
  if (L1LowSupported) {
    PciSegmentOr32 (RpBase + R_PCH_PCIE_CFG_PCIEPMECTL, (UINT32) B_PCH_PCIE_CFG_PCIEPMECTL_L1LE);
  } else {
    PciSegmentAnd32 (RpBase + R_PCH_PCIE_CFG_PCIEPMECTL, (UINT32) ~B_PCH_PCIE_CFG_PCIEPMECTL_L1LE);
  }

  if (L1LowSupported || L1ssEnabled) {
    ///
    /// f.  Set Dxx:Fn:420h[0] to 1b prior to L1 enabling if any L1substate is enabled (including L1.LOW)
    ///
    PciSegmentOr32 (RpBase + R_PCH_PCIE_CFG_PCIEPMECTL, B_PCH_PCIE_CFG_PCIEPMECTL_L1FSOE);
  }
}

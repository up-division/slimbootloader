## @file
# This file is used to provide board specific image information.
#
#  Copyright (c) 2018 - 2021, Intel Corporation. All rights reserved.<BR>
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
#

##
# Import Modules
#
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.append (os.path.join('..', '..'))
from BuildLoader import BaseBoard, STITCH_OPS, FLASH_REGION_TYPE, HASH_USAGE
from BuildLoader import IPP_CRYPTO_OPTIMIZATION_MASK, IPP_CRYPTO_ALG_MASK, HASH_TYPE_VALUE

class Board(BaseBoard):
    def __init__(self, *args, **kwargs):

        super(Board, self).__init__(*args, **kwargs)

        self.VERINFO_IMAGE_ID       = 'SBL_TGL'
        self.VERINFO_PROJ_MAJOR_VER = 0
        self.VERINFO_PROJ_MINOR_VER = 8
        self.VERINFO_SVN            = 1
        self.VERINFO_BUILD_DATE     = time.strftime("%m/%d/%Y")

        self.BOARD_NAME           = 'tgl'
        self._EXTRA_INC_PATH      = ['Silicon/TigerlakePkg/FspBin']
        self._FSP_PATH_NAME       = 'Silicon/TigerlakePkg/FspBin'
        self.BOARD_PKG_NAME       = 'TigerlakeBoardPkg'
        self.SILICON_PKG_NAME     = 'TigerlakePkg'
        self.PCH_PKG_NAME         = 'TigerlakePchPkg'
        self.FSP_IMAGE_ID         = 'TGLI-FSP'

        self.PCI_EXPRESS_BASE     = 0xC0000000
        self.PCI_IO_BASE          = 0x00002000
        self.PCI_MEM32_BASE       = 0x80000000
        self.ACPI_PM_TIMER_BASE   = 0x1808
        self.LOADER_ACPI_RECLAIM_MEM_SIZE = 0x000090000

        self.FLASH_BASE_ADDRESS   = 0xFF000000
        self.FLASH_BASE_SIZE      = (self.FLASH_LAYOUT_START - self.FLASH_BASE_ADDRESS)

        self.HAVE_FIT_TABLE       = 1
        self.HAVE_VBT_BIN         = 1
        self.HAVE_VERIFIED_BOOT   = 1
        self.HAVE_MEASURED_BOOT   = 1
        self.HAVE_ACPI_TABLE      = 1
        self.HAVE_PSD_TABLE       = 1
        self.ENABLE_VTD           = 1
        # To enable source debug, set 1 to self.ENABLE_SOURCE_DEBUG
        self.ENABLE_SOURCE_DEBUG  = 0
        # If ENABLE_SOURCE_DEBUG is disabled, SKIP_STAGE1A_SOURCE_DEBUG will be ignored
        self.SKIP_STAGE1A_SOURCE_DEBUG  = 0
        self.ENABLE_SPLASH        = 1
        self.ENABLE_FRAMEBUFFER_INIT    = 1
        self.ENABLE_FAST_BOOT     = 0
        self.HAVE_FUSA            = 1

        if self.HAVE_FIT_TABLE:
            self.FIT_ENTRY_MAX_NUM  = 10

        if self.ENABLE_FAST_BOOT:
            self.ENABLE_SPLASH              = 0
            self.ENABLE_FRAMEBUFFER_INIT    = 0
            self.RELEASE_MODE               = 1
            self.HAVE_VERIFIED_BOOT         = 0
            self.HAVE_MEASURED_BOOT         = 0
            self.VERIFIED_BOOT_HASH_MASK    = 0

        # RSA2048 or RSA3072
        self._RSA_SIGN_TYPE          = 'RSA3072'

        # 'SHA2_256' or 'SHA2_384'
        self._SIGN_HASH              = 'SHA2_384'

        # 0x01 for SHA2_256 or 0x02 for SHA2_384
        self.SIGN_HASH_TYPE          = HASH_TYPE_VALUE[self._SIGN_HASH]

        # 0x0010  for SM3_256 | 0x0008 for SHA2_512 | 0x0004 for SHA2_384 | 0x0002 for SHA2_256 | 0x0001 for SHA1
        self.IPP_HASH_LIB_SUPPORTED_MASK   = IPP_CRYPTO_ALG_MASK['SHA2_384'] | IPP_CRYPTO_ALG_MASK['SHA2_256']
        # G9 for 384 | W7 Opt for SHA384| Ni  Opt for SHA256| V8 Opt for SHA256
        self.ENABLE_CRYPTO_SHA_OPT  = IPP_CRYPTO_OPTIMIZATION_MASK['SHA256_NI'] | IPP_CRYPTO_OPTIMIZATION_MASK['SHA384_W7']

        # Key configuration
        self._MASTER_PRIVATE_KEY    = 'KEY_ID_MASTER' + '_' + self._RSA_SIGN_TYPE
        self._CFGDATA_PRIVATE_KEY   = 'KEY_ID_CFGDATA' + '_' + self._RSA_SIGN_TYPE
        self._CONTAINER_PRIVATE_KEY = 'KEY_ID_CONTAINER' + '_' + self._RSA_SIGN_TYPE

        # 0 - PCH UART0, 1 - PCH UART1, 2 - PCH UART2, 0xFF - EC UART 0x3F8
        self.DEBUG_PORT_NUMBER = 0xFF

        if self.RELEASE_MODE:
            self.STAGE1A_SIZE         = 0x0000D000
            self.STAGE1B_SIZE         = 0x000B0000
            self.STAGE2_SIZE          = 0x00070000
            self.STAGE2_FD_SIZE       = 0x000E0000
            self.PAYLOAD_SIZE         = 0x00024000
        else:
            self.STAGE1A_SIZE         = 0x00016000
            self.STAGE1B_SIZE         = 0x00180000
            self.STAGE2_SIZE          = 0x00110000
            self.STAGE2_FD_SIZE       = 0x00200000
            self.PAYLOAD_SIZE         = 0x00080000

        if self.ENABLE_SOURCE_DEBUG:
            self.STAGE1B_SIZE += 0x4000

        self.ENABLE_FWU           = 1
        self.ENABLE_SMBIOS        = 1
        self.ENABLE_CSME_UPDATE   = 1

        # CSME update library is required to enable this option and will be available as part of CSME kit
        self.BUILD_CSME_UPDATE_DRIVER   = 0

        self.STAGE1B_XIP          = 1

        self.STAGE2_FD_BASE       = 0x01000000

        self.STAGE1_STACK_SIZE    = 0x00030000
        self.STAGE1_DATA_SIZE     = 0x00010000

        self.PAYLOAD_EXE_BASE     = 0x00B00000

        if len(self._PAYLOAD_NAME.split(';')) > 1:
            # EPAYLOAD is specified
            self.EPAYLOAD_SIZE      = 0x00160000
            self.UEFI_VARIABLE_SIZE = 0x00040000
        else:
            # EPAYLOAD does not exist, create a dummy one
            self.EPAYLOAD_SIZE      = 0x1000
            self.UEFI_VARIABLE_SIZE = 0x1000

        self.UCODE_SIZE           = 0x00038000
        self.MRCDATA_SIZE         = 0x00010000
        self.CFGDATA_SIZE         = 0x00002000
        self.KEYHASH_SIZE         = 0x00001000
        self.VARIABLE_SIZE        = 0x00002000
        self.SBLRSVD_SIZE         = 0x00001000
        self.FWUPDATE_SIZE        = 0x00020000 if self.ENABLE_FWU else 0
        self.OS_LOADER_FD_SIZE    = 0x0004D000
        self.OS_LOADER_FD_NUMBLK  = self.OS_LOADER_FD_SIZE // self.FLASH_BLOCK_SIZE

        self.TOP_SWAP_SIZE        = 0x080000
        self.REDUNDANT_SIZE       = 0x360000

        self.SIIPFW_SIZE = 0x1000
        self.ENABLE_TCC_TUNING = 1
        if self.ENABLE_TCC_TUNING:
            self.TCCB_SIZE = 0x00001000
            self.TCCC_SIZE = 0x00001000
            self.TCCM_SIZE = 0x00004000
            self.TCCT_SIZE = 0x00003000
            self.SIIPFW_SIZE += self.TCCC_SIZE + self.TCCB_SIZE + self.TCCM_SIZE + self.TCCT_SIZE

        self.ENABLE_TSN_MAC_ADDRESS = 1
        if self.ENABLE_TSN_MAC_ADDRESS:
            self.TMAC_SIZE = 0x00001000
            self.SIIPFW_SIZE += self.TMAC_SIZE

        Redundant_Components_Size = self.UCODE_SIZE + self.STAGE2_SIZE + self.STAGE1B_SIZE + self.FWUPDATE_SIZE + self.CFGDATA_SIZE + self.KEYHASH_SIZE
        if Redundant_Components_Size > self.REDUNDANT_SIZE:
            raise Exception ('Redundant region size 0x%x is smaller than required components size 0x%x!' % (self.REDUNDANT_SIZE, Redundant_Components_Size))
        self.NON_REDUNDANT_SIZE   = 0x2B2000 + self.SIIPFW_SIZE
        self.NON_VOLATILE_SIZE    = 0x001000
        self.SLIMBOOTLOADER_SIZE  = (self.TOP_SWAP_SIZE + self.REDUNDANT_SIZE) * 2 + self.NON_REDUNDANT_SIZE + self.NON_VOLATILE_SIZE

        self.PLD_HEAP_SIZE        = 0x04000000
        self.PLD_STACK_SIZE       = 0x00020000
        self.PLD_RSVD_MEM_SIZE    = 0x00500000

        self.DIAGNOSTICACM_SIZE   = 0x00001000
        # TBD: ACM/KM/BPM Size, as of Sep 2017
        # ACM size is updated to 256KB, KM size is fixed 0x400, BPM size is fixed 0x600
        self.KM_SIZE              = 0x00000400
        self.BPM_SIZE             = 0x00000600
        self.ACM_SIZE             = 0x00040000 + self.KM_SIZE + self.BPM_SIZE
        # adjust ACM_SIZE to meet 256KB alignment (to align 256KB ACM size)
        if self.ACM_SIZE > 0:
            acm_top = self.FLASH_LAYOUT_START - self.STAGE1A_SIZE - self.DIAGNOSTICACM_SIZE
            acm_btm = acm_top - self.ACM_SIZE
            acm_btm = (acm_btm & 0xFFFC0000)
            self.ACM_SIZE     = acm_top - acm_btm

        self.CFGDATA_REGION_TYPE  = FLASH_REGION_TYPE.BIOS
        self.SPI_IAS_REGION_TYPE  = FLASH_REGION_TYPE.BIOS

        self.LOADER_RSVD_MEM_SIZE = 0x500000

        self.CFG_DATABASE_SIZE    = self.CFGDATA_SIZE

        # _CFGDATA_INT_FILE - Internal cfg data is generally used for internal boards like MRBs, RVPs etc.
        # _CFGDATA_EXT_FILE - External cfg data is for the customer boards to populate new data on top of the internal defaults.
        # Cfg data dlt files for nternal boards could also put into external cfg data if want to update cfg data for these platforms
        # for test purpose. Based on the platform id, relevant data is populated for each platform.
        self._CFGDATA_INT_FILE = []
        self._CFGDATA_EXT_FILE = ['CfgData_Ext_Dummy.dlt', 'CfgData_Int_Tglu_Ddr4.dlt', 'CfgData_Int_Tglu_DdrLp4.dlt']

    def GetPlatformDsc (self):
        dsc = {}
        dsc['LibraryClasses.%s' % self.BUILD_ARCH] = [
            'LoaderLib|Platform/CommonBoardPkg/Library/LoaderLib/LoaderLib.inf',
            'PchInfoLib|Silicon/$(PCH_PKG_NAME)/Library/PchInfoLib/PchInfoLib.inf',
            'PchPcrLib|Silicon/$(PCH_PKG_NAME)/Library/PchPcrLib/PchPcrLib.inf',
            'PchP2sbLib|Silicon/$(PCH_PKG_NAME)/Library/PchP2sbLib/PchP2sbLib.inf',
            'PchSbiAccessLib|Silicon/$(PCH_PKG_NAME)/Library/PchSbiAccessLib/PchSbiAccessLib.inf',
            'PlatformHookLib|Silicon/$(SILICON_PKG_NAME)/Library/PlatformHookLib/PlatformHookLib.inf',
            'GpioLib|Silicon/$(PCH_PKG_NAME)/Library/GpioLib/GpioLib.inf',
            'PchSpiLib|Silicon/CommonSocPkg/Library/PchSpiLib/PchSpiLib.inf',
            'SpiFlashLib|Silicon/CommonSocPkg/Library/SpiFlashLib/SpiFlashLib.inf',
            'VtdLib|Silicon/$(SILICON_PKG_NAME)/Library/VTdLib/VTdLib.inf',
            'ShellExtensionLib|Platform/$(BOARD_PKG_NAME)/Library/ShellExtensionLib/ShellExtensionLib.inf',
            'IgdOpRegionLib|Silicon/CommonSocPkg/Library/IgdOpRegionLib/IgdOpRegionLib.inf',
            'HeciInitLib|Silicon/$(PCH_PKG_NAME)/Library/HeciInitLib/HeciInitLib.inf',
            'BootGuardLib|Silicon/CommonSocPkg/Library/BootGuardLibCBnT/BootGuardLibCBnT.inf',
            'BdatLib|Silicon/$(SILICON_PKG_NAME)/Library/BdatLib/BdatLib.inf',
            'ItbtPcieRpLib|Silicon/$(SILICON_PKG_NAME)/Library/ItbtPcieRpLib/ItbtPcieRpLib.inf',
            'PsdLib|Silicon/$(SILICON_PKG_NAME)/Library/PsdLib/PsdLib.inf',
            'MeExtMeasurementLib|Silicon/$(PCH_PKG_NAME)/Library/MeExtMeasurementLib/MeExtMeasurementLib.inf',
            'BasePchPciBdfLib|Silicon/$(PCH_PKG_NAME)/Library/BasePchPciBdfLib/BasePchPciBdfLib.inf'
        ]

        if self.BUILD_CSME_UPDATE_DRIVER:
            dsc['LibraryClasses.%s' % self.BUILD_ARCH].append ('MeFwUpdateLib|Silicon/$(PCH_PKG_NAME)/Library/MeFwUpdateLib/MeFwUpdateLib.inf')

        dsc['PcdsFeatureFlag.%s' % self.BUILD_ARCH] = [
            'gPlatformTigerLakeTokenSpaceGuid.PcdFusaEnabled | $(HAVE_FUSA)'
        ]
        return dsc

    def GetKeyHashList (self):
        # Define a set of new key used for different purposes
        # The key is either key id or public key PEM format or private key PEM format
        pub_key_list = [
          (
            # Key for verifying Config data blob
            HASH_USAGE['PUBKEY_CFG_DATA'],
            'KEY_ID_CFGDATA' + '_' + self._RSA_SIGN_TYPE
          ),
          (
            # Key for verifying firmware update
            HASH_USAGE['PUBKEY_FWU'],
            'KEY_ID_FIRMWAREUPDATE' + '_' + self._RSA_SIGN_TYPE
          ),
          (
            # Key for verifying container header
            HASH_USAGE['PUBKEY_CONT_DEF'],
            'KEY_ID_CONTAINER' + '_' + self._RSA_SIGN_TYPE
          ),
          (
            # Use RSA2048 key for verifying OS image signed with RSA2048
            HASH_USAGE['PUBKEY_OS'],
            'KEY_ID_OS1_PUBLIC_RSA2048'
          ),
          (
            # Use RSA3072 key for verifying OS image signed with RSA3072
            HASH_USAGE['PUBKEY_OS'],
            'KEY_ID_OS1_PUBLIC_RSA3072'
          ),
        ]
        return pub_key_list

    def GetContainerList (self):
        container_list = []
        container_list_auth_type = self._RSA_SIGN_TYPE + '_'+ self._SIGNING_SCHEME[4:] + '_' + self._SIGN_HASH
        container_list.append (
          # Name | Image File             |    CompressAlg  | AuthType                        | Key File                        | Region Align   | Region Size |  Svn Info
          # ========================================================================================================================================================
          ('IPFW',      'SIIPFW.bin',          '',     container_list_auth_type,   'KEY_ID_CONTAINER'+'_'+self._RSA_SIGN_TYPE,        0,          0     ,        0),   # Container Header
        )

        if self.ENABLE_TCC_TUNING:
            container_list.append (
              ('TCCB','',      'Lz4',     container_list_auth_type,   'KEY_ID_CONTAINER_COMP'+'_'+self._RSA_SIGN_TYPE,    0,   self.TCCB_SIZE,        0),   # TCC Buffers
            )
            container_list.append (
               ('TCCC','',    'Lz4',     container_list_auth_type,  'KEY_ID_CONTAINER_COMP'+'_'+self._RSA_SIGN_TYPE,    0,   self.TCCC_SIZE,        0),   # TCC Cache Config
            )
            container_list.append (
               ('TCCM','',  'Lz4',     container_list_auth_type,  'KEY_ID_CONTAINER_COMP'+'_'+self._RSA_SIGN_TYPE,    0,   self.TCCM_SIZE,        0),   # TCC PTCM
            )
            container_list.append (
              ('TCCT','',      'Lz4',     container_list_auth_type,   'KEY_ID_CONTAINER_COMP'+'_'+self._RSA_SIGN_TYPE, 0,   self.TCCT_SIZE,      0),   # TCC Tuning
            )

        if self.ENABLE_TSN_MAC_ADDRESS:
            container_list.append (
              ('TMAC','',     'Lz4',     container_list_auth_type,   'KEY_ID_CONTAINER_COMP'+'_'+self._RSA_SIGN_TYPE,     0,   self.TMAC_SIZE,        0),   # TSN MAC Address
            )

        return [container_list]

    def GetOutputImages (self):
        # define extra images that will be copied to output folder
        img_list = ['SlimBootloader.txt',
                    'FlashMap.txt',
                    'CfgDataStitch.py',
                    'CfgDataDef.yaml']
        return img_list

    def GetImageLayout (self):
        img_list = []

        acm_flag = 0 if self.ACM_SIZE > 0 else STITCH_OPS.MODE_FILE_IGNOR
        fwu_flag = 0 if self.ENABLE_FWU else STITCH_OPS.MODE_FILE_IGNOR
        diagnosticacm_flag = 0 if self.DIAGNOSTICACM_SIZE > 0 else STITCH_OPS.MODE_FILE_IGNOR
        cfg_flag = 0 if len(self._CFGDATA_EXT_FILE) > 0 and self.CFGDATA_REGION_TYPE == FLASH_REGION_TYPE.BIOS else STITCH_OPS.MODE_FILE_IGNOR

        if len(self._CFGDATA_EXT_FILE) > 0 and self.CFGDATA_REGION_TYPE == FLASH_REGION_TYPE.PLATFORMDATA:
            img_list.extend ([
                ('CFGDATA_PDR.bin', [
                    ('CFGDATA.bin',   '',   self.CFGDATA_SIZE,     STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
            ])

        img_list.extend ([
                ('NON_VOLATILE.bin', [
                    ('SBLRSVD.bin',    ''        , self.SBLRSVD_SIZE,  STITCH_OPS.MODE_FILE_NOP, STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
                ('NON_REDUNDANT.bin', [
                    ('SIIPFW.bin'   ,  ''        , self.SIIPFW_SIZE,   STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('VARIABLE.bin',     '',       self.VARIABLE_SIZE, STITCH_OPS.MODE_FILE_NOP, STITCH_OPS.MODE_POS_TAIL),
                    ('UEFIVARIABLE.bin', '',       self.UEFI_VARIABLE_SIZE,  STITCH_OPS.MODE_FILE_NOP, STITCH_OPS.MODE_POS_TAIL),
                    ('MRCDATA.bin',      '',       self.MRCDATA_SIZE,  STITCH_OPS.MODE_FILE_NOP, STITCH_OPS.MODE_POS_TAIL),
                    ('EPAYLOAD.bin',     '',       self.EPAYLOAD_SIZE, STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('PAYLOAD.bin',      'Lz4',    self.PAYLOAD_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
                ('REDUNDANT_A.bin', [
                    ('UCODE.bin'    ,  ''        , self.UCODE_SIZE,    STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE2.fd'    ,  'Lz4'     , self.STAGE2_SIZE,   STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('FWUPDATE.bin' ,  'Lzma'    , self.FWUPDATE_SIZE, STITCH_OPS.MODE_FILE_PAD | fwu_flag,  STITCH_OPS.MODE_POS_TAIL),
                    ('CFGDATA.bin'  , ''         , self.CFGDATA_SIZE,  STITCH_OPS.MODE_FILE_PAD | cfg_flag, STITCH_OPS.MODE_POS_TAIL),
                    ('KEYHASH.bin'  , ''         , self.KEYHASH_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE1B_A.fd' ,  ''        , self.STAGE1B_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),

                ('REDUNDANT_B.bin', [
                    ('UCODE.bin'    ,  ''        , self.UCODE_SIZE,    STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE2.fd'    ,  'Lz4'     , self.STAGE2_SIZE,   STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('FWUPDATE.bin' ,  'Lzma'    , self.FWUPDATE_SIZE, STITCH_OPS.MODE_FILE_PAD | fwu_flag,  STITCH_OPS.MODE_POS_TAIL),
                    ('CFGDATA.bin'  , ''         , self.CFGDATA_SIZE,  STITCH_OPS.MODE_FILE_PAD | cfg_flag, STITCH_OPS.MODE_POS_TAIL),
                    ('KEYHASH.bin'  , ''         , self.KEYHASH_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE1B_B.fd' ,  ''        , self.STAGE1B_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
                ('TOP_SWAP_A.bin', [
                    ('ACM.bin',         '',     self.ACM_SIZE,      STITCH_OPS.MODE_FILE_NOP | acm_flag,  STITCH_OPS.MODE_POS_TAIL),
                    ('DIAGNOSTICACM.bin',        '',     self.DIAGNOSTICACM_SIZE,     STITCH_OPS.MODE_FILE_NOP | diagnosticacm_flag, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE1A_A.fd',    '',     self.STAGE1A_SIZE,  STITCH_OPS.MODE_FILE_NOP,             STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
                ('TOP_SWAP_B.bin', [
                    ('ACM.bin',         '',     self.ACM_SIZE,      STITCH_OPS.MODE_FILE_NOP | acm_flag,  STITCH_OPS.MODE_POS_TAIL),
                    ('DIAGNOSTICACM.bin',        '',     self.DIAGNOSTICACM_SIZE,     STITCH_OPS.MODE_FILE_NOP | diagnosticacm_flag, STITCH_OPS.MODE_POS_TAIL),
                    ('STAGE1A_B.fd',    '',     self.STAGE1A_SIZE,  STITCH_OPS.MODE_FILE_NOP,             STITCH_OPS.MODE_POS_TAIL),
                    ]
                ),
                ('SlimBootloader.bin', [
                    ('NON_VOLATILE.bin'  , '' , self.NON_VOLATILE_SIZE,  STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ('NON_REDUNDANT.bin' , '' , self.NON_REDUNDANT_SIZE, STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ('REDUNDANT_B.bin'   , '' , self.REDUNDANT_SIZE,     STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ('REDUNDANT_A.bin'   , '' , self.REDUNDANT_SIZE,     STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ('TOP_SWAP_B.bin'    , '' , self.TOP_SWAP_SIZE,      STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ('TOP_SWAP_A.bin'    , '' , self.TOP_SWAP_SIZE,      STITCH_OPS.MODE_FILE_PAD, STITCH_OPS.MODE_POS_HEAD),
                    ]
                ),
        ])

        return img_list

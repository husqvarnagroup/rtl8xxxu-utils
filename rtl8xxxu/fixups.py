MASK_NAMES_TO_IGNORE = {
    'SYS_CFG_SW_OFFLOAD_EN': '',
    'SYS_CFG_SPS_LDO_SEL': '',
    'SYS_CFG_TRP_BT_EN': '',
    'SYS_CFG_RTL_ID': '',
    'MODE_AG_CHANNEL_20MHZ': '',
    'HPON_FSM_BONDING_1T2R': '',
    'SYS_CFG_CHIP_VER' : 'Overlapping mask is also defined',
    'WMAC_TRXPTCL_CTL_BW_MASK': 'More detailed bit description exists',
    'CCK0_AFE_RX_ANT_AB': 'Defined twice',
    'CCK0_AFE_RX_ANT_B': 'Defined twice',
    'MODE_AG_BW_20MHZ_8723B': 'Overlaps with more relevant definition',
    'MODE_AG_BW_40MHZ_8723B': 'Overlaps with more relevant definition',
    'MODE_AG_BW_80MHZ_8723B': 'Overlaps with more relevant definition',
    'SYS_CFG_VENDOR_ID': 'Contained in SYS_CFG_VENDOR_EXT_MASK',
    'LEDCFG0_DPDT_SELECT': 'Not available on RTL8188CUS'
}

# Registers which are problematic and not relevant for RTL8188CUS
REGISTER_NAMES_TO_IGNORE = {
    'REG_HOST_SUSP_CNT': 'Defined twice',
    'REG_Q0_INFO': 'Also know as REG_VOQ_INFO',
    'REG_Q1_INFO': 'Also know as REG_VIQ_INFO',
    'REG_Q2_INFO': 'Also know as REG_BEQ_INFO',
    'REG_Q3_INFO': 'Also know as REG_BKQ_INFO',
    'REG_MACID_SLEEP_3_8732B': 'Also know as REG_INIDATA_RATE_SEL',
    'REG_EARLY_MODE_CONTROL_8188E': 'Also know as REG_MACID_DROP_8732A',
    'REG_MACID_SLEEP_2_8732B': 'Also know as REG_MACID_DROP_8732A',
    'REG_MBSSID_BCN_SPACE': 'Also know as REG_BCN_INTERVAL',
    'REG_FPGA0_XAB_RF_SW_CTRL': 'Covered by REG_FPGA0_X{A,B}_RF_SW_CTRL',
    'REG_FPGA0_XCD_RF_SW_CTRL': 'Covered by REG_FPGA0_X{C,D}_RF_SW_CTRL',
    'REG_FPGA0_XAB_RF_PARM': 'Covered by REG_FPGA0_X{A,B}_RF_PARM',
    'REG_FPGA0_XCD_RF_PARM': 'Covered by REG_FPGA0_X{C,D}_RF_PARM',
    'REG_RX_DMA_CTRL_8723B': 'Not available on RTL8188CUS'
}

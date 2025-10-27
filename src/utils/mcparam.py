# AXI PARAM
AXI_ADDRW               = 36 
AXI_DATAW               = 256                                  
AXI_STRBW               = 32    # AXI_PARAM.AXI_DATAW 
AXI_IDW                 = 8
AXI_LENW                = 8
AXI_SIZEW               = 4     # log2Floor(AXI_PARAM.AXI_DATAW/8)
AXI_BURSTW              = 2     # AXI a*burst 
AXI_LOCKW               = 2     # AXI a*lock w
AXI_USERW               = 1
AXI_CACHEW              = 4     # AXI a*cache 
AXI_PROTW               = 3     # AXI a*prot w
AXI_QOSW                = 4     # AXI a*qos wi
AXI_RESPW               = 2     # AXI *resp wi
OCPAR_ADDR_PAR_WIDTH    = 8     # AXI awparity w 


# UI PARAM
UI_ADDRW                = 36    # AXI address
UI_DATAW                = 512   # AXI *data wi
UI_STRBW                = 64    # AXI wstrb wi


TOKEN_WIDTH             = 10
ADDR_WIDTH              = 36 
DATA_WIDTH              = 512    
STRB_WIDTH              = 64  
PRI_WIDTH               = 1

#SplitCmdIO parameter
RANK_WIDTH              = 1 ,
BG_WIDTH                = 2 ,
BANK_WIDTH              = 2 ,
ROW_WIDTH               = 18,
COL_WIDTH               = 10,

ABITS                   = 18 # ROW_WIDTH
BABITS                  = 2  # BANK_WIDTH
BGBITS                  = 2  # BG_WIDTH
GROUPBITS               = 2 
COLBITS                 = 10 # COL_WIDTH
RKBITS                  = 1  # RANK_WIDTH
DATABITS                = 25 # DATA_WIDTH
CKEBITS                 = 1 
ODTBITS                 = 1 
TOKENBITS               = 17 # scg token width

RdDataEnWidth           = 32 # nanhu 32 yanqihu 16
RdDataCsNWidth          = 32 
RdDataVldWidth          = 32 
RdDataDbiWidth          = 32 
WrDataEnWidth           = 32 #nanhu 32 yanqihu 16
WrDataCsNWidth          = 32 
CMDBITS                 = 3  

ResetNWidth             = 1
CsNWidth                = 1 
ActNWidth               = 1
RasNWidth               = 1
CasNWidth               = 1
WeNWidth                = 1
CidBITS                 = 1
PARAMETERWIDTH          = 5

McParamWidth            = 16
TXN_FIFO_DEPTH          = 16
CMD_FIFO_DEPTH          = 16

tZQINTVL_Witdh          = 32


RLmax                   =  10
trddata_en              =  2 
tphy_rdcslat            =  2 
tphy_rdlat              =  4 
Wlmax                   =  10

lengthWidthMAX          = 20
tphy_wrcslatMAX         = 10
tphy_rdcslatMAX         = 10
ODTMAX                  = 48

BANK_NUM                = 4  
BURST_LENGTH            = UI_DATAW // AXI_DATAW


BURST1                  = 0x0
BURST2                  = 0x1
BURST4                  = 0x2
BURST8                  = 0x3
BURST16                 = 0x4
BURST32                 = 0x5
BURST64                 = 0x6
BURST128                = 0x7

axiMasterPortDict = {
  # Write address channel
  "io_awio_awid": 0, 
  "io_awio_awaddr": 0,
  "io_awio_awlen": 0,
  "io_awio_awsize": 0,
  "io_awio_awburst": 0,
  "io_awio_awuser": 0,
  "io_awio_awqos": 0,
  "io_awio_awvalid": 0,
  # Write data channel
  "io_wio_wid": 0,
  "io_wio_wuser": 0,
  "io_wio_wdata": 0,
  "io_wio_wstrb": 0,
  "io_wio_wlast": 0,
  "io_wio_wvalid": 0,
  # Wrirtes response channel
  "io_bio_bready": 0,
  # Read address channel
  "io_ario_arid": 0,
  "io_ario_araddr": 0,
  "io_ario_arlen": 0,
  "io_ario_arsize": 0,
  "io_ario_arburst": 0,
  "io_ario_aruser": 0,
  "io_ario_arqos": 0,
  "io_ario_arvalid": 0,
  # Read data channel
  "io_rio_rready": 0
}

uiSlavePortDict = {
  # Write address channel
  "io_ui_awio_ready": 0,
  # Write data channel
  "io_ui_wio_ready": 0,
  # Read address channel
  "io_ui_ario_ready": 0,
  # Read data channel
  "io_ui_rio_valid": 0,
  "io_ui_rio_bits_rdata": 0,
  "io_ui_rio_bits_rtoken": 0,
}


axi2uiDict = {
  "clock": 0,
  "reset": 0,
  "io_awio_awid": 0,
  "io_awio_awaddr": 0,
  "io_awio_awlen": 0,
  "io_awio_awsize": 0,
  "io_awio_awburst": 0,
  "io_awio_awuser": 0,
  "io_awio_awqos": 0,
  "io_awio_awvalid": 0,
  "io_awio_awready": 0,
  "io_wio_wid": 0,
  "io_wio_wuser": 0,
  "io_wio_wdata": 0,
  "io_wio_wstrb": 0,
  "io_wio_wlast": 0,
  "io_wio_wvalid": 0,
  "io_wio_wready": 0,
  "io_bio_bid": 0,
  "io_bio_bresp": 0,
  "io_bio_buser": 0,
  "io_bio_bvalid": 0,
  "io_bio_bready": 0,
  "io_ario_arid": 0,
  "io_ario_araddr": 0,
  "io_ario_arlen": 0,
  "io_ario_arsize": 0,
  "io_ario_arburst": 0,
  "io_ario_aruser": 0,
  "io_ario_arqos": 0,
  "io_ario_arvalid": 0,
  "io_ario_arready": 0,
  "io_rio_rid": 0,
  "io_rio_ruser": 0,
  "io_rio_rdata": 0,
  "io_rio_rresp": 0,
  "io_rio_rlast": 0,
  "io_rio_rvalid": 0,
  "io_rio_rready": 0,
  "io_ui_awio_ready": 0,
  "io_ui_awio_valid": 0,
  "io_ui_awio_bits_addr": 0,
  "io_ui_awio_bits_token": 0,
  "io_ui_awio_bits_pri": 0,
  "io_ui_wio_ready": 0,
  "io_ui_wio_valid": 0,
  "io_ui_wio_bits_wdata": 0,
  "io_ui_wio_bits_wstrb": 0,
  "io_ui_ario_ready": 0,
  "io_ui_ario_valid": 0,
  "io_ui_ario_bits_addr": 0,
  "io_ui_ario_bits_token": 0,
  "io_ui_ario_bits_pri": 0,
  "io_ui_rio_ready": 0,
  "io_ui_rio_valid": 0,
  "io_ui_rio_bits_rdata": 0,
  "io_ui_rio_bits_rtoken": 0,
  "io_a2uregio_axiRdCmdCnt": 0,
  "io_a2uregio_axiWrCmdCnt": 0,
  "io_a2uregio_uiRdCmdCnt": 0,
  "io_a2uregio_uiWrCmdCnt": 0,
  "io_a2uregio_uiRbCmdCnt": 0,
  "io_a2uregio_readyStall": 0,
  "io_a2uregio_tokenCnt": 0
}


def strbdata(data, strb, length):
    result = 0
    for i in range(length):
        if strb & (1 << i):
            result |= (data & (0xff << i * 8))
    return result

def combine_data(data: list, length):
    result = 0
    for i in range(len(data)):
        result |= data[i] << (i * length)
    return result

def split_data(data, length):
    result = []
    mask = (1 << length) - 1
    while data > 0:
        result.append(data & mask)
        data >>= length
    return result
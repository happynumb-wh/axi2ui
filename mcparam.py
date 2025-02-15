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

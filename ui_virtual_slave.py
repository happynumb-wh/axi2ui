from axi2ui import *
import random
import mcparam
from axi2ui import *
from scorebord import *

class ui_virtual_slave:

    class Status(Enum):
        IDLE = 0
        ARIO = 1
        AWIO = 2
        RIO = 3
        WIO = 4
        
    def __init__(self, dut:DUTosmc_axi_top, scorebord:scoreBord):
        self.readCnt = 0
        self.writeCnt = 0
        self.rstatus = self.Status.IDLE
        self.wstatus = self.Status.IDLE
        self.inPrepareReadData = 0
        self.inPrepareWriteData = 0
        self.readToken = []
        self.writeToken = []
        self.readRecord = {}
        self.writeRecord = {}
        self.dut = dut
        self.scorebord = scorebord
        # Delay cycle to 
        self.writeDelay = 0
        self.readDelay = 0
        self.waitWriteDelay = 0
        self.waitReadDelay = 0
        self.cycle = 0
        
    def setWriteDelay(self, cycle):
        self.writeDelay = cycle
    
    def setReadDelay(self, cycle):
        self.readDelay = cycle
    
    # axi2ui hand shake with ui
    def awrioHandShake(self, cycle):
        if self.dut.io_ui_ario_valid.value:
            if self.dut.io_ui_ario_ready.value:
                self.dut.io_ui_ario_ready.value = 0
                self.inPrepareReadData = 1
            else:
                # Record addr and token
                Token = self.dut.io_ui_ario_bits_token.value
                Addr = self.dut.io_ui_ario_bits_addr.value
                
                # if self.readRecord.get(Token) == None:
                self.readRecord[Token] = [Addr, Token]
                self.readToken = [Addr, Token]  

                # Handle This read request
                self.dut.io_ui_ario_ready.value = 1
                self.readCnt += 1
                
                self.rstatus = self.Status.RIO
        if self.dut.io_ui_awio_valid.value:
            if self.dut.io_ui_awio_ready.value:
                self.dut.io_ui_awio_ready.value = 0
                self.inPrepareWriteData = 1
            else:
                # Record addr and token
                Token = self.dut.io_ui_awio_bits_token.value
                Addr = self.dut.io_ui_awio_bits_addr.value
                
                self.writeRecord[Token] = [Addr, Token]
                self.writeToken = [Addr, Token]      

                # Handle This write request
                self.dut.io_ui_awio_ready.value = 1
                self.writeCnt += 1
                self.wstatus = self.Status.WIO

    def strbdata(self, data, strb):
        result = 0
        for i in range(mcparam.UI_STRBW):
            if strb & (1 << i):
                result |= (data & (0xff << i * 8))
        return result
    
    def wrioHandShake(self, cycle):
        if self.inPrepareWriteData:
            if self.dut.io_ui_wio_valid.value:
                if self.dut.io_ui_wio_ready.value:
                    self.inPrepareWriteData = 0
                    self.dut.io_ui_wio_ready.value = 0
                    self.scorebord.writeMemory(self.writeToken[0], self.writeToken[2])
                else:
                    if self.writeDelay != 0:
                        self.waitWriteDelay += 1
                        if self.waitWriteDelay == self.writeDelay:
                            self.waitWriteDelay = 0
                        else:
                            return

                    self.dut.io_ui_wio_ready.value = 1
                    # store the data in token
                    self.writeToken.append(self.strbdata(self.dut.io_ui_wio_bits_wdata.value, self.dut.io_ui_wio_bits_wstrb.value))
                    self.scorebord.commitWrite(self.writeToken[1], self.writeToken[0], self.writeToken[2])
                    # print("Write addr:", hex(self.writeToken[0]))
                    
        if self.inPrepareReadData:
            if self.dut.io_ui_rio_ready.value:
                if self.dut.io_ui_rio_valid.value:
                    self.inPrepareReadData = 0
                    self.dut.io_ui_rio_valid.value = 0
                else: 
                # Delay to back
                    if self.readDelay != 0:
                        self.waitReadDelay += 1
                        if self.waitReadDelay == self.readDelay:
                            self.waitReadDelay = 0
                        else:
                            return
                    self.dut.io_ui_rio_valid.value = 1
                    rdata = self.scorebord.readMemory(self.readToken[0])
                    self.dut.io_ui_rio_bits_rdata.value = rdata
                    self.dut.io_ui_rio_bits_rtoken.value = self.readToken[1]
                    self.scorebord.readAddRecord(self.readToken[1], self.readToken[0], rdata)
                    
                    # print("Read addr:", hex(self.readToken[0]), hex(rdata))
import mcparam
from axi2ui import *
from scorebord import *
from enum import Enum
import random 

class axi_virtual_master:
    # status
    class Status(Enum):
        IDLE = 0
        ARIO = 1
        AWIO = 2
        RIO = 3
        WIO = 4
        WBACK = 5
        
    def __init__(self, dut:DUTosmc_axi_top, scorebord:scoreBord):
        # meta data
        self.rstatus = self.Status.IDLE
        self.wstatus = self.Status.IDLE
        self.wburst_counter = 0
        self.rburst_counter = 0
        self.rburst_data = []
        self.wburst_data = []
        self.araddr = 0
        self.awaddr = 0
        self.ard_trans = 0
        self.awr_trans = 0
        self.rd_trans = 0
        self.wr_trans = 0
        self.burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
        self.dut = dut
        # record data
        self.dataCompare = {}
        self.rholdcycle = 0
        self.wholdcycle = 0
        
        self.scorebord = scorebord

        self.writeIndex = 0
    # reset all signal
    def reset(self):
        self.dut.io_wio_wlast.value = 0
        self.dut.io_wio_wvalid.value = 0
        self.dut.io_awio_awvalid.value = 0
        self.dut.io_ario_arvalid.value = 0
        self.dut.io_rio_rready.value = 0
        self.dut.io_bio_bready.value = 0
        self.dut.io_awio_awburst.value = 0
        self.dut.io_ario_arburst.value = 0
        
        
        self.dut.io_awio_awaddr.value = 0
        self.dut.io_awio_awlen.value = 0
        self.dut.io_awio_awsize.value = 0
        self.dut.io_ario_araddr.value = 0
        self.dut.io_ario_arlen.value = 0
        self.dut.io_ario_arsize.value = 0

    def createWriteData(self):
        self.writeIndex = (self.writeIndex + 1) % 16
        index = self.writeIndex
        result = 0
        for i in range(mcparam.AXI_DATAW // 4):
            result |= (index << (4 * i))
            # print(hex(result))
        # print(result)
        return result
    
    def combine_data(self, data: list):
        result = 0
        for i in range(len(data)):
            result |= data[i] << (i * mcparam.AXI_DATAW)
        return result
    
    # AXI aradder
    def axi_ario(self, araddr, arburst, arsize, arlen):
        self.rholdcycle = 0
        self.ard_trans += 1
        self.rburst_counter = 0        
        self.rstatus = self.Status.ARIO
        self.dut.io_ario_arvalid.value = 1
        self.dut.io_ario_araddr.value = araddr
        self.dut.io_ario_arburst.value = arburst        
        self.dut.io_ario_arsize.value = arsize
        self.dut.io_ario_arlen.value = arlen
        self.araddr = araddr
        
    # AXI awadder
    def axi_awio(self, awaddr, awburst, awsize, awlen):
        self.wholdcycle = 0
        self.awr_trans += 1
        self.wburst_counter = 0
        self.wstatus = self.Status.AWIO
        self.dut.io_awio_awvalid.value = 1
        self.dut.io_awio_awaddr.value = awaddr
        self.dut.io_awio_awburst.value = awburst
        self.dut.io_awio_awsize.value = awsize
        self.dut.io_awio_awlen.value = awlen
        self.awaddr = awaddr
        
    # AXI master read 
    def axiReadMachine(self, cycle):
        if self.rstatus ==  self.Status.IDLE:
            self.rstatus = self.Status.IDLE
        
        elif self.rstatus == self.Status.ARIO:
            # arvalid must be ok
            assert self.dut.io_ario_arvalid.value, "Must set ario_arvalid when read data channel"
            
            if self.dut.io_ario_arvalid.value and self.dut.io_ario_arready.value:
                self.rholdcycle = 0
                self.dut.io_ario_arvalid.value = 0
                # master ready to recv data
                # next cycle will recv data
                self.dut.io_rio_rready.value = 1
                self.rstatus = self.Status.RIO            
            elif not self.dut.io_ario_arready.value:
                self.rstatus == self.Status.ARIO
                self.rholdcycle += 1
                if self.rholdcycle > 10000:
                    print("Error: axi AR hold to long!")
                    self.dut.Finish()
                    exit(0)
        
        elif self.rstatus == self.Status.RIO:
            # rready ok
            assert self.dut.io_rio_rready.value, "Must set io_rio_rready when read data"
            if self.dut.io_rio_rvalid.value and self.dut.io_rio_rready.value:
                # Collect data
                self.rburst_data.append(self.dut.io_rio_rdata.value)
                self.rburst_counter += 1
                self.rd_trans += 1
                # Last read data
                if self.dut.io_rio_rlast.value:
                    # Burst data Finish
                    # print(f"Read data: {hex(self.rburst_data[0])}, {hex(self.rburst_data[1])}")
                    self.scorebord.commitRead(self.araddr, self.combine_data(self.rburst_data))
                    assert self.rburst_counter == self.burst_length
                    self.rburst_counter = 0
                    self.dut.io_rio_rready.value = 0
                    self.rburst_data = []
                    self.rstatus = self.Status.IDLE
    
    # axi master write
    def axiWriteMachine(self, cycle):
        if self.wstatus ==  self.Status.IDLE:
            self.wstatus = self.Status.IDLE
        elif self.wstatus == self.Status.AWIO:
            assert self.dut.io_awio_awvalid.value, "Must set awio_awvalid when writ channel address ok"
            if self.dut.io_awio_awvalid.value and self.dut.io_awio_awready.value:
                self.wholdcycle = 0
                self.dut.io_awio_awvalid.value = 0
                # master ready to send data
                self.dut.io_wio_wvalid.value = 1
                # print(f"addr: {hex(self.awaddr)}, Write {self.wburst_counter}")
                # If we prepare to switch to WIO, set wdata now
                self.dut.io_wio_wdata.value = random.randint(0, 2**mcparam.AXI_DATAW - 1) # self.createWriteData() 
                
                self.wstatus = self.Status.WIO
            elif not self.dut.io_awio_awready.value:
                self.wstatus = self.Status.AWIO
                self.wholdcycle += 1
                if self.wholdcycle > 10000:
                    print("Error: axi AW hold to long!")
                    self.dut.Finish()
                    exit(0)
        elif self.wstatus == self.Status.WIO:
            assert self.dut.io_wio_wvalid.value, "Must set wio_wvalid when writ channel ok"
            if self.dut.io_wio_wvalid.value and self.dut.io_wio_wready.value:
                self.wburst_counter += 1
                if self.wburst_counter == self.burst_length - 1:
                    # in first write data cycle set last signal
                    self.dut.io_wio_wlast.value = 1
                self.wburst_data.append(self.dut.io_wio_wdata.value)
                
                if self.wburst_counter == self.burst_length:
                    # last cycle to send write data
                    self.scorebord.writeAddRecord(self.awaddr, self.combine_data(self.wburst_data))
                    # print(f"DEBUG: {self.wburst_counter} {hex(self.awaddr)}, data: {hex(self.combine_data(self.wburst_data))}")
                    self.dut.io_wio_wvalid.value = 0
                    self.dut.io_wio_wlast.value = 0
                    self.dut.io_bio_bready.value = 1
                    self.wburst_counter = 0
                    self.wstatus = self.Status.WBACK
                else:
                    self.dut.io_wio_wdata.value = self.createWriteData()
        elif self.wstatus == self.Status.WBACK:
            assert self.dut.io_bio_bready.value, "Must set bio_bready when back write channel"
            
            if self.dut.io_bio_bvalid.value and self.dut.io_bio_bready.value:
                self.dut.io_bio_bready.value = 0
                self.wburst_data = []
                self.wstatus = self.Status.IDLE            
     
    # def axi_addrhandshake(self, cycle):
    #     # Addr channel Handshake ok
    #     if self.rstatus != self.Status.ARIO and self.wstatus != self.Status.AWIO:
    #         return
        
    #     if self.dut.io_awio_awvalid.value and self.dut.io_awio_awready.value:
    #         self.wholdcycle = 0
    #         self.dut.io_awio_awvalid.value = 0
    #         # master ready to send data
    #         self.dut.io_wio_wvalid.value = 1
    #         print(f"addr: {hex(self.awaddr)}, Write {self.wburst_counter}")
    #         self.wstatus = self.Status.WIO
            
    #     if self.dut.io_ario_arvalid.value and self.dut.io_ario_arready.value:
    #         self.rholdcycle = 0
    #         self.dut.io_ario_arvalid.value = 0
    #         # master ready to recv data
    #         self.dut.io_rio_rready.value = 1
    #         self.rstatus = self.Status.RIO
        
    #     if self.dut.io_awio_awvalid.value and (not self.dut.io_awio_awready.value):
    #         self.wholdcycle += 1
        
    #     if self.dut.io_ario_arvalid.value and (not self.dut.io_ario_arready.value):
    #         self.rholdcycle +=1
        
        
    #     if self.rholdcycle > 10000 or self.wholdcycle > 10000:
    #         print("Ar/Aw hold too long !!!")
    #         self.dut.Finish()
    #         exit(1)
            

    
    # # every read cycle
    # def every_read_cycle(self, cycle):
    #     # not waiting data
    #     if self.rstatus != self.Status.RIO:
    #         return
        
    #     if self.dut.io_rio_rvalid.value and self.dut.io_rio_rready.value:
    #         # Collect data
    #         self.rburst_data.append(self.dut.io_rio_rdata.value)
    #         self.rburst_counter += 1
    #         self.rd_trans += 1
             
    #         if self.dut.io_rio_rlast.value:
    #             # Burst data Finish
    #             print(f"Read data: {hex(self.rburst_data[0])}, {hex(self.rburst_data[1])}")
    #             self.scorebord.commitRead(self.araddr, self.combine_data(self.rburst_data))
    #             self.rburst_data = []
    #             self.rstatus = self.Status.IDLE
    #             assert self.rburst_counter == self.burst_length
    #             self.rburst_counter = 0
    #             self.dut.io_rio_rready.value = 0
                
    #         # print(f"recv data {hex(self.dut.io_rio_rdata.value)}")
                    
    # def every_write_cycle(self, cycle):
        
    #     # Clear wlast
    #     if self.dut.io_wio_wlast.value:
    #         print(self.wburst_counter)
    #         if self.dut.io_wio_wvalid.value and self.dut.io_wio_wready.value:
    #             pass
    #         else:
    #             print("fuck")
    #         self.dut.io_wio_wlast.value = 0
            
    #         if self.wburst_counter == self.burst_length:
    #             self.scorebord.writeAddRecord(self.awaddr, self.combine_data(self.wburst_data))
    #             print(f"DEBUG: {self.wburst_counter} {hex(self.awaddr)}, data: {hex(self.combine_data(self.wburst_data))}")
    #             self.wstatus = self.Status.WBACK
    #             self.dut.io_wio_wvalid.value = 0
    #             self.dut.io_bio_bready.value = 1
    #             self.wburst_counter = 0
    #             return 
    #     # not waiting data
    #     if self.wstatus != self.Status.WIO:
    #         return

    #     if self.dut.io_wio_wvalid.value and self.dut.io_wio_wready.value:
    #         print(f"Write: addr: {hex(self.awaddr)}, {self.wburst_counter}, {self.burst_length}")
    #         # when wburst_counter == burst_length, clear wvalid
            
            
    #         # Collect data
    #         self.wburst_counter += 1
    #         self.wr_trans += 1
    #         self.dut.io_wio_wdata.value = self.createWriteData() #random.randint(0, 2**mcparam.AXI_DATAW - 1)
    #         self.wburst_data.append(self.dut.io_wio_wdata.value)
            
    #         if self.wburst_counter == self.burst_length:
    #             print(f"set last : {hex(self.awaddr)}")
    #             self.dut.io_wio_wlast.value = 1
    #         else:
    #             self.dut.io_wio_wlast.value = 0            
    # def wrio_finish(self, cycle):
    #     if self.wstatus != self.Status.WBACK:
    #         return
        
    #     if self.dut.io_bio_bvalid.value and self.dut.io_bio_bready.value:
    #         self.dut.io_bio_bready.value = 0
    #         self.wburst_data = []
    #         self.wstatus = self.Status.IDLE
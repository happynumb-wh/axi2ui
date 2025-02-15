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

    # AXI aradder
    def axi_ario(self, araddr, arburst, arsize, arlen):
        self.rholdcycle = 0
        self.ard_trans += 1
        self.rstatus = self.Status.ARIO
        self.rburst_counter = 0
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
        self.wstatus = self.Status.AWIO
        self.wburst_counter = 0
        self.dut.io_awio_awvalid.value = 1
        self.dut.io_awio_awaddr.value = awaddr
        self.dut.io_awio_awburst.value = awburst
        self.dut.io_awio_awsize.value = awsize
        self.dut.io_awio_awlen.value = awlen
        self.awaddr = awaddr
        
    def axi_addrhandshake(self, cycle):
        # Addr channel Handshake ok
        if self.rstatus != self.Status.ARIO and self.wstatus != self.Status.AWIO:
            return
        
        if self.dut.io_awio_awvalid.value and self.dut.io_awio_awready.value:
            self.wholdcycle = 0
            self.dut.io_awio_awvalid.value = 0
            # master ready to send data
            self.dut.io_wio_wvalid.value = 1
            self.wstatus = self.Status.WIO
            
        if self.dut.io_ario_arvalid.value and self.dut.io_ario_arready.value:
            self.rholdcycle = 0
            self.dut.io_ario_arvalid.value = 0
            # master ready to recv data
            self.dut.io_rio_rready.value = 1
            self.rstatus = self.Status.RIO
        
        if self.dut.io_awio_awvalid.value and (not self.dut.io_awio_awready.value):
            self.wholdcycle += 1
        
        if self.dut.io_ario_arvalid.value and (not self.dut.io_ario_arready.value):
            self.rholdcycle +=1
        
        
        if self.rholdcycle > 10000 or self.wholdcycle > 10000:
            print("Ar/Aw hold too long !!!")
            self.dut.Finish()
            exit(1)
            
    def combine_data(self, data: list):
        result = 0
        for i in range(len(data)):
            result |= data[i] << (i * mcparam.AXI_DATAW)
        return result
    
    # every read cycle
    def every_read_cycle(self, cycle):
        # not waiting data
        if self.rstatus != self.Status.RIO:
            return
        
        if self.dut.io_rio_rvalid.value and self.dut.io_rio_rready.value:
            # Collect data
            self.rburst_data.append(self.dut.io_rio_rdata.value)
            self.rburst_counter += 1
            self.rd_trans += 1
             
            if self.dut.io_rio_rlast.value:
                # Burst data Finish
                print(f"Read data: {hex(self.rburst_data[0])}, {hex(self.rburst_data[1])}")
                self.scorebord.commitRead(self.araddr, self.combine_data(self.rburst_data))
                self.rburst_data = []
                self.rstatus = self.Status.IDLE
                assert self.rburst_counter == self.burst_length
                self.dut.io_rio_rready.value = 0
                
            # print(f"recv data {hex(self.dut.io_rio_rdata.value)}")
                    
    def every_write_cycle(self, cycle):
        
        # Clear wlast
        if self.dut.io_wio_wlast.value:
            self.dut.io_wio_wlast.value = 0
            
        # not waiting data
        if self.wstatus != self.Status.WIO:
            return

        if self.dut.io_wio_wvalid.value and self.dut.io_wio_wready.value:
            # when wburst_counter == burst_length, clear wvalid
            if self.wburst_counter == self.burst_length:
                self.scorebord.writeAddRecord(self.awaddr, self.combine_data(self.wburst_data))
                self.wstatus = self.Status.WBACK
                self.dut.io_wio_wvalid.value = 0
                self.dut.io_bio_bready.value = 1
                self.wburst_counter = 0
                return             
            
            # Collect data
            self.wburst_counter += 1
            self.wr_trans += 1
            self.dut.io_wio_wdata.value = random.randint(0, 2**mcparam.AXI_DATAW - 1)
            self.wburst_data.append(self.dut.io_wio_wdata.value)
            
            if self.wburst_counter == self.burst_length:
                self.dut.io_wio_wlast.value = 1
            else:
                self.dut.io_wio_wlast.value = 0            
    def wrio_finish(self, cycle):
        if self.wstatus != self.Status.WBACK:
            return
        
        if self.dut.io_bio_bvalid.value and self.dut.io_bio_bready.value:
            self.dut.io_bio_bready.value = 0
            self.wburst_data = []
            self.wstatus = self.Status.IDLE
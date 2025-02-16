import mcparam
from axi2ui import *
from enum import Enum
import random

class scoreBord:
    def __init__(self,dut: DUTosmc_axi_top):
        self.virtualMemory = {}
        self.dut = dut
        self.readRecord = []
        self.writeRecord = []
    
    
    def writeMemory(self, addr, data):
        self.virtualMemory[addr] = data
    # Read memory
    def readMemory(self, addr):
        if self.virtualMemory.get(addr) == None:
            self.virtualMemory[addr] = random.randint(0, 2**mcparam.UI_DATAW - 1)
        return self.virtualMemory[addr]

    def readMemoryCompare(self, addr, data):
        if self.virtualMemory.get(addr) == None:
            print(f"Error: Address {addr} not found")
    
    # Add a read record to score bord
    def readAddRecord(self, token, addr, rdata):
        self.readRecord.append([token, addr, rdata])
    
    # Add a write record to score bord
    def writeAddRecord(self, addr, wdata):
        self.writeRecord.append([addr, wdata])
    
    
    def commitWrite(self, token, addr, data):
        for i in range(len(self.writeRecord)):
            if self.writeRecord[i][0] == addr:
                if self.writeRecord[i][1] == data:
                    print(f"Write commit: token: {token} addr: {hex(addr)} success")
                else:
                    print(f"Write commit error: token: {token} addr: {hex(addr)} failed")
                    print(f"axi write data: {hex(self.writeRecord[i][1])}")
                    print(f"ui write data: {hex(data)}")
                    self.dut.Finish()
                    exit(0)
                self.writeRecord.pop(i)
                return
                
    def commitRead(self, addr, data):
        for i in range(len(self.readRecord)):
            if self.readRecord[i][1] == addr:
                if self.readRecord[i][2] == data:
                    print(f"Read commit: token: {self.readRecord[i][0]} addr: {hex(addr)} success")
                else:
                    print(f"Read commit error: token: {self.readRecord[i][0]} addr:  {hex(addr)} failed")
                    print(f"axi read data: {hex(data)}")
                    print(f"ui read data: {hex(self.readRecord[i][2])}")
                    self.dut.Finish()
                    exit(0)
                self.readRecord.pop(i)
                return
        pass
    
    def compare(self, addr, data):
        pass
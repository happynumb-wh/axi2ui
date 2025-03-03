from toffee import *
from env.axi2uiBundle import *
from env.message import *
from env.axiAgent import *
from env.uiAgent import *
from axi2ui import *
import toffee

class axi2uiEnv(Env):
    def __init__(self, axiBundle: axiMasterBundle, uiBundle: uiSlaveBundle, dut: DUTosmc_axi_top):
        super().__init__()
        self.readBundle = axiBundle.readBundle
        self.writeBundle = axiBundle.writeBundle
        self.memory = scoreBord()
        self.axiReadAgent = axiReadAgent(axiBundle.readBundle)
        self.axiWriteAgent = axiWriteAgent(axiBundle.writeBundle)
        self.uiReadAgent = uiReadAgent(uiBundle.readBundle, self.memory)
        self.uiWriteAgent = uiWriteAgent(uiBundle.writeBundle, self.memory)
        self.dut = dut
        self.handler = []
    
    # Create a deamon to handle the axi and ui channel
    async def envDeamon(self):
        self.handler.append(toffee.create_task(self.axiReadAgent.handleRio()))
        self.handler.append(toffee.create_task(self.axiWriteAgent.handleWio()))
        self.handler.append(toffee.create_task(self.axiWriteAgent.handleBio()))
        self.handler.append(toffee.create_task(self.uiReadAgent.handleArio()))
        self.handler.append(toffee.create_task(self.uiReadAgent.handleRio()))
        self.handler.append(toffee.create_task(self.uiWriteAgent.handleAwio()))
        self.handler.append(toffee.create_task(self.uiWriteAgent.handleWio()))
        self.handler.append(toffee.create_task(self.readCommit()))
        self.handler.append(toffee.create_task(self.writeCommit()))
        
    
    async def reset(self):
        self.dut.reset.value = 1
        await self.readBundle.step(100)
        self.dut.reset.value = 0
        await self.readBundle.step(10)

    
    
    async def readCommit(self):
        while True:
            if len(self.axiReadAgent.queue) == 0 or len(self.uiReadAgent.queue) == 0:
                await self.readBundle.step(1)
                continue
            axiItem = self.axiReadAgent.queue[0]
            uiItem = self.uiReadAgent.queue[0]
            
            assert axiItem[0] == uiItem[0], "Read address not match"
            if axiItem[2] and axiItem[1] and uiItem[1] and uiItem[2]:
                if axiItem[3] != uiItem[3]:
                    print(f"Read data not match: addr: {hex(axiItem[0])} Token: {hex(axiItem[5])}")
                    self.dut.Finish()
                    exit(0)
                self.axiReadAgent.finishRequest += 1
                self.axiReadAgent.queue.pop(0)
                self.uiReadAgent.queue.pop(0)
            await self.readBundle.step(1)
            
    async def writeCommit(self):
        while True:
            if len(self.axiWriteAgent.queue) == 0 or len(self.uiWriteAgent.queue) == 0:
                await self.writeBundle.step(1)
                continue
            axiItem = self.axiWriteAgent.queue[0]
            uiItem = self.uiWriteAgent.queue[0]
            
            assert axiItem[0] == uiItem[0], "Write address not match"
            if axiItem[3] and axiItem[2] and axiItem[1] and uiItem[1] and uiItem[2]:
                if axiItem[4] != uiItem[3]:
                    print(f"Write data not match: addr: {hex(axiItem[0])}")
                    self.dut.Finish()
                    exit(0)
                self.axiWriteAgent.finishRequest += 1
                self.axiWriteAgent.queue.pop(0)
                self.uiWriteAgent.queue.pop(0)
            await self.writeBundle.step(1)
                 
    async def Finish(self):
        while True:
            if self.axiReadAgent.finishRequest == self.axiReadAgent.arioRequest and self.axiWriteAgent.finishRequest == self.axiWriteAgent.awioRequest:
                break
            await ClockCycles(self.dut, 1)
    
    def __del__(self):
        self.dut.Finish()
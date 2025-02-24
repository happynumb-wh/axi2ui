from toffee import *
from utils import mcparam
from env.message import *
from env.axi2uiBundle import *
from env.scorebord import *


class uiReadAgent(Agent):
    '''
    Agent for the read channel
    '''
    def __init__(self, bundle: uiReadBundle, memory: scoreBord):
        super().__init__(bundle)
        self.bundle = bundle
        self.message = axi2uiReadMessage(bundle)
        self.memory = memory
        self.queue = []
        self.rioDelay =  0

    def setRioDelay(self, delay):
        self.rioDelay = delay

    @driver_method()
    async def handleArio(self):
        '''
        queue: [addr, ario, rio, rdata, token]
        '''
        while True:
            port = {
                'ario': {
                    "ready": 1
                }
            }
            self.bundle.assign(port)
            await Value(self.bundle.ario.valid, 1)
            self.queue.append([self.bundle.ario.bits_addr.value, 0, 0, 0, self.bundle.ario.bits_token.value])
            port['ario']['ready'] = 0
            self.bundle.assign(port)
            self.queue[-1][1] = 1
            await self.bundle.step(1)
    
    @driver_method()
    async def handleRio(self):
        while True:
            if len(self.queue) == 0:
                await self.bundle.step(1)
                continue
            
            for item in self.queue:
                if item[1] == 1 and item[2] == 0:
                    break
            else:
                await self.bundle.step(1)
                continue

            port = {
                'rio': {
                    'valid': 1
                }
            }            
            port['rio']['bits_rdata'] = self.memory.readMemory(item[0])
            port['rio']['bits_rtoken'] = item[4]
            
            if self.rioDelay > 0:
                await self.bundle.step(self.rioDelay)
            self.bundle.assign(port)
            await Value(self.bundle.rio.ready, 1)
            port['rio']['valid'] = 0
            self.bundle.assign(port)
            item[3] = port['rio']['bits_rdata']
            item[2] = 1
            await self.bundle.step(1)            
        
        
class uiWriteAgent(Agent):
    '''
    Agent for the write channel
    '''
    def __init__(self, bundle: uiWriteBundle, memory: scoreBord):
        super().__init__(bundle)
        self.bundle = bundle
        self.message = axi2uiReadMessage(bundle)
        self.memory = memory
        self.queue = []

    @driver_method()
    async def handleAwio(self):
        '''
        queue: [addr, awio, wio, wdata, wstrb, token]
        '''
        while True:
            port = {
                'awio': {
                    "ready": 1
                }
            }
            self.bundle.assign(port)
            await Value(self.bundle.awio.valid, 1)
            self.queue.append([self.bundle.awio.bits_addr.value, 0, 0, 0, 0, self.bundle.awio.bits_token.value])
            port['awio']['ready'] = 0
            self.bundle.assign(port)
            self.queue[-1][1] = 1
            await self.bundle.step(1)
            
    @driver_method()
    async def handleWio(self):
        while True:
            port = {
                'wio': {
                    'ready': 1
                }
            }
            if len(self.queue) == 0:
                await self.bundle.step(1)
                continue
            
            for item in self.queue:
                if item[1] == 1 and item[2] == 0:
                    break
            else:
                await self.bundle.step(1)
                continue
            
            self.bundle.assign(port)
            await Value(self.bundle.wio.valid, 1)
            # Write data
            item[3] = self.bundle.wio.bits_wdata.value
            item[4] = self.bundle.wio.bits_wstrb.value
            port['wio']['ready'] = 0
            self.bundle.assign(port)
            item[2] = 1
            self.memory.writeMemory(item[0], mcparam.strbdata(item[3], item[4], mcparam.UI_STRBW))
            await self.bundle.step(1)
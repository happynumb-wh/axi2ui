from toffee import *
from utils import mcparam
from env.message import *
from env.axi2uiBundle import *
import random

class axiWriteAgent(Agent):
    '''
    Agent for the write channel
    '''
    def __init__(self, bundle: axiWriteBundle):
        super().__init__(bundle)
        self.awioRequest = 0
        self.finishRequest = 0
        self.bundle = bundle
        self.message = axi2uiWriteMessage(bundle)
        self.queue = []

    @driver_method()
    async def handleAwio(self, port: dict):
        '''
        Queue: [addr, awio, wio, bio, wdata, token]
        '''
        port['awio']['awvalid'] = 1
        # {
        #     "awid": 0,
        #     "awaddr": addr,
        #     "awlen": awlen,
        #     "awsize": awsize,
        #     "awburst": awburst,
        #     "awuser": 0,
        #     "awqos": 0,
        #     "awvalid": 1
        # }
        self.bundle.assign(port)
        await Value(self.bundle.awio.awready, 1)
        self.queue.append([port['awio']['awaddr'], 0, 0, 0, 0, 0])
        self.awioRequest += 1
        port['awio']['awvalid'] = 0
        self.bundle.assign(port)
        # Write addr handle ok
        self.queue[-1][1] = 1
    
    @driver_method()
    async def handleWio(self):

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
                'wio': {
                    'wid': 0,
                    'wuser': 0,
                    'wdata': 0,
                    'wstrb': 0,
                    'wlast': 0,
                    'wvalid': 0
                }
            }            
            
            port['wio']['wvalid'] = 1
            port['wio']['wstrb'] = 0xffffffff
            port['wio']['wdata'] = random.randint(0, 2**mcparam.AXI_DATAW - 1)
            # fixme: set write data
            # set data
            self.bundle.assign(port)
            # await self.bundle.step(1)
            await Value(self.bundle.wio.wready, 1)
            data = []
            while True:
                if len(data) == mcparam.BURST_LENGTH:
                    break
                               
                if self.bundle.wio.wready.value:
                    if self.bundle.wio.wlast.value:
                        data.append(mcparam.strbdata(self.bundle.wio.wdata.value, self.bundle.wio.wstrb.value, mcparam.AXI_STRBW))
                        port['wio']['wlast'] = 0 
                        port['wio']['wvalid'] = 0
                        assert len(data) == 2, "Wlast finish recv data"
                        item[4] = mcparam.combine_data(data, mcparam.AXI_DATAW)
                        item[2] = 1                    
                    else:
                        # fixme set data
                        port['wio']['wdata'] = random.randint(0, 2**mcparam.AXI_DATAW - 1)
                        data.append(self.bundle.wio.wdata.value)
                        if len(data) == mcparam.BURST_LENGTH - 1: # 
                            port['wio']['wlast'] = 1
                else:
                    await Value(self.bundle.wio.wready, 1)

                self.bundle.assign(port)
                await self.bundle.step(1)


    @driver_method()
    async def handleBio(self):
        while True:
            if len(self.queue) == 0:
                await self.bundle.step(1)
                continue
            
            for item in self.queue:
                if item[1] == 1 and item[2] == 1 and item[3] == 0:
                    break
            else:
                await self.bundle.step(1)
                continue       
                 
            port = {
                'bio': {
                    'bready': 1
                }
            }
            self.bundle.assign(port)
            await Value(self.bundle.bio.bvalid, 1)
            item[3] = 1
            port['bio']['bready'] = 0
            self.bundle.assign(port)
            await self.bundle.step(1)
            
    
    async def Write(self, awaddr, awlen, awsize, awburst):
        port = {
            'awio': {
                'awid': 0,
                'awaddr': awaddr,
                'awlen': awlen,
                'awsize': awsize,
                'awburst': awburst,
                'awuser': 0,
                'awqos': 0,
                'awvalid': 0                     
            }
        }
        await self.handleAwio(port)
        
    
class axiReadAgent(Agent):
    '''
    Agent for the read channel
    '''
    def __init__(self, bundle: axiReadBundle):
        super().__init__(bundle)
        self.arioRequest = 0
        self.finishRequest = 0
        self.bundle = bundle
        self.message = axi2uiReadMessage(bundle)
        self.queue = []      
    
    @driver_method()
    async def handleArio(self, port: dict):
        '''
        Queue: [addr, ario, rio, rdata[2], token]
        '''
        port['ario']['arvalid'] = 1
        # {
        #     "arid": 0,
        #     "araddr": addr,
        #     "arlen": awlen,
        #     "arsize": awsize,
        #     "arburst": awburst,
        #     "aruser": 0,
        #     "arqos": 0,
        #     "arvalid": 1
        # }
        self.bundle.assign(port)
        await Value(self.bundle.ario.arready, 1)
        self.queue.append([port['ario']['araddr'], 0, 0, 0, 0])
        self.arioRequest += 1
        port['ario']['arvalid'] = 0
        self.bundle.assign(port)
        # Read addr handle ok
        self.queue[-1][1] = 1
    
    
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
                    'rready': 1
                }
            }
            self.bundle.assign(port)
            # await self.bundle.step(1)
            await Value(self.bundle.rio.rvalid, 1)
            data = []
            while True:
                if len(data) == mcparam.BURST_LENGTH: # 
                    break
                if self.bundle.rio.rvalid.value:
                    data.append(self.bundle.rio.rdata.value)
                    if self.bundle.rio.rlast.value:
                        item[2] = 1
                        item[3] = mcparam.combine_data(data, mcparam.AXI_DATAW)
                        # clear rready
                        port['rio']['rready'] = 0  
                else:
                    await Value(self.bundle.rio.rvalid, 1)
                    continue
                
                self.bundle.assign(port)
                await self.bundle.step(1)

        
    
    async def Read(self, araddr, arlen, arsize, arburst):
        port = {
            'ario': {
                'arid': 0,
                'araddr': araddr,
                'arlen': arlen,
                'arsize': arsize,
                'arburst': arburst,
                'aruser': 0,
                'arqos': 0,
                'arvalid': 0                 
            }
        }
        
        # wait finish
        await self.handleArio(port)

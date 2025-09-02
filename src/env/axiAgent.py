from toffee import *
from utils import mcparam
from env.message import *
from env.axi2uiBundle import *
import random
import sys
from enum import *
from axi2ui import *


class WriteIndex(IntEnum):
    AWID = 0
    ADDR  = 1
    AWIO = 2
    WIO = 3
    BIO = 4
    WDATA = 5
    TOKEN = 6
    WRLEN = 7
    WRSIZE = 8
    LENGTH = 9

class axiWriteAgent(Agent):
    '''
    Agent for the write channel
    '''
    def __init__(self, bundle: axiWriteBundle, dut: DUTosmc_axi_top):
        super().__init__(bundle)
        self.awioRequest = 0
        self.finishRequest = 0
        self.bundle = bundle
        self.message = axi2uiWriteMessage(bundle)
        self.queue = []
        self.dut = dut
        self.wioDelay = 0
        self.wioRandomDelay = False
        self.awioDelay = 0
        self.awioRandomDelay = False
        self.bioDelay = 0
        self.bioRandomDelay = False
        self.waitForWready = 0

    def setWioDelay(self, delay, random=False):
        self.wioDelay = delay
        self.wioRandomDelay = random
        
    def setAwioDelay(self, delay, random=False):
        self.awioDelay = delay
        self.awioRandomDelay = random
        
    def setBioDelay(self, delay, random=False):
        self.bioDelay = delay
        self.bioRandomDelay = random
    
    def setWaitForWready(self, value):
        self.waitForWready = value

    @driver_method()
    async def handleAwio(self, port: dict):
        '''
        Queue: [awid, addr, awio, wio, bio, wdata, token, wrlen, wrsize]
        '''
        port['awio']['awvalid'] = 1
        # {
        #     "awid": awid,
        #     "awaddr": addr,
        #     "awlen": awlen,
        #     "awsize": awsize,
        #     "awburst": awburst,
        #     "awuser": 0,
        #     "awqos": 0,
        #     "awvalid": 1
        # }
        if self.awioDelay:
            if self.awioRandomDelay:
                await self.bundle.step(random.randint(1, self.awioDelay))
            else:
                await self.bundle.step(self.awioDelay)
        self.bundle.assign(port)
        await Value(self.bundle.awio.awready, 1)
        for item in self.queue:
            if item[WriteIndex.AWIO] == 0:
                item[WriteIndex.ADDR] = port['awio']['awaddr']
                item[WriteIndex.AWID] = port['awio']['awid']
                assert item[WriteIndex.WRLEN] == port['awio']['awlen'] + 1, "Write length not match"
                assert item[WriteIndex.WRSIZE] == 2**port['awio']['awsize'] * 8, "Write size not match"
                break
        else:
            item = [0] * WriteIndex.LENGTH
            item[WriteIndex.ADDR] = port['awio']['awaddr']
            item[WriteIndex.AWID] = port['awio']['awid']
            item[WriteIndex.WRLEN] = port['awio']['awlen'] + 1
            item[WriteIndex.WRSIZE] = 2**port['awio']['awsize'] * 8
            self.queue.append(item)
        self.awioRequest += 1
        port['awio']['awvalid'] = 0
        self.bundle.assign(port)
        # Write addr handle ok
        item[WriteIndex.AWIO] = 1
        # await self.bundle.step(1)
        return item
    
    @driver_method()
    async def handleWio(self):
        while True:
            wioNew = 0
           
            port = {
                'wio': {
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

            if self.wioDelay:
                if self.wioRandomDelay:
                    await self.bundle.step(random.randint(1, self.wioDelay))
                else:
                    await self.bundle.step(self.wioDelay)
            if self.waitForWready:
                await Value(self.bundle.wio.wready, 1, 0)   # this may cause deadlock, we just test it anyhow
            # set data
            self.bundle.assign(port)
            # await self.bundle.step(1)
            await Value(self.bundle.wio.wready, 1)
            # We get function first
            for item in self.queue:
                if item[WriteIndex.AWIO] == 1 and item[WriteIndex.WIO] == 0:
                    break
               
            else:
                item = [0] * WriteIndex.LENGTH
                item[WriteIndex.WRLEN] = BURST_LENGTH
                item[WriteIndex.WRSIZE] = 2**BURST32 * 8
                wioNew = 1  
            
            if wioNew:
                self.queue.append(item)
            
            data = []
            length = item[7]
            while True:
                if len(data) == length:
                    break
                               
                if self.bundle.wio.wready.value:
                    if self.bundle.wio.wlast.value:
                        data.append(mcparam.strbdata(self.bundle.wio.wdata.value, self.bundle.wio.wstrb.value, mcparam.AXI_STRBW))
                        port['wio']['wlast'] = 0 
                        port['wio']['wvalid'] = 0
                        assert len(data) == length, "Wlast finish recv data"
                        item[WriteIndex.WDATA] = mcparam.combine_data(data, mcparam.AXI_DATAW)
                        item[WriteIndex.WIO] = 1
                    else:
                        # fixme set data
                        port['wio']['wdata'] = random.randint(0, 2**mcparam.AXI_DATAW - 1)
                        data.append(self.bundle.wio.wdata.value)
                        if len(data) == length - 1: # 
                            port['wio']['wlast'] = 1
                else:
                    await Value(self.bundle.wio.wready, 1)
                    continue

                self.bundle.assign(port)
                await self.bundle.step(1)

           
    @driver_method()
    async def handleBio(self):
        while True:
            if len(self.queue) == 0:
                await self.bundle.step(1)
                continue
            
            port = {
                'bio': {
                    'bready': 1
                }
            }
            if self.bioDelay:
                if self.bioRandomDelay:
                    await self.bundle.step(random.randint(1, self.bioDelay))
                else:
                    await self.bundle.step(self.bioDelay)
            self.bundle.assign(port)
            await Value(self.bundle.bio.bvalid, 1)
            
            for item in self.queue:
                # if item[WriteIndex.AWID] == self.bundle.bio.bid.value and item[WriteIndex.AWIO] == 1 and item[WriteIndex.WIO] == 1 and item[WriteIndex.BIO] == 0:
                if item[WriteIndex.AWIO] == 1 and item[WriteIndex.WIO] == 1 and item[WriteIndex.BIO] == 0:
                    break
            else:
                assert False, "B channel return unmatched bid"
            
            if item[WriteIndex.AWID] != self.bundle.bio.bid.value:
                print(self.bundle.bio.bid.value)
                print(item[WriteIndex.AWID])
                self.dut.Finish()
                sys.exit(0)
            
            item[WriteIndex.BIO] = 1
            port['bio']['bready'] = 0
            self.bundle.assign(port)
            await self.bundle.step(1)
            
    
    async def Write(self, awid, awaddr, awlen, awsize, awburst):
        port = {
            'awio': {
                'awid': awid,
                'awaddr': awaddr,
                'awlen': awlen,
                'awsize': awsize,
                'awburst': awburst,
                'awuser': 0,
                'awqos': 0,
                'awvalid': 0                     
            }
        }
        return await self.handleAwio(port)



class ReadIndex(IntEnum):
    ARID = 0
    ADDR  = 1
    ARIO = 2
    RIO = 3
    RDATA = 4
    TOKEN = 5
    ARLEN = 6
    ARSIZE = 7
    LENGTH = 8
    
class axiReadAgent(Agent):
    '''
    Agent for the read channel
    '''
    def __init__(self, bundle: axiReadBundle, dut: DUTosmc_axi_top):
        super().__init__(bundle)
        self.arioRequest = 0
        self.finishRequest = 0
        self.bundle = bundle
        self.message = axi2uiReadMessage(bundle)
        self.queue = []      
        self.dut = dut
        self.rioDelay = 0
        
    def setRioDelay(self, delay):
        self.rioDelay = delay
    
    @driver_method()
    async def handleArio(self, port: dict):
        '''
        Queue: [arid, addr, ario, rio, rdata, token, arlen, arsize]
        '''
        port['ario']['arvalid'] = 1
        # {
        #     "arid": arid,
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
        item = [0] * ReadIndex.LENGTH
        item[ReadIndex.ARID] = port['ario']['arid']
        item[ReadIndex.ADDR] = port['ario']['araddr']
        item[ReadIndex.ARLEN] = port['ario']['arlen'] + 1
        item[ReadIndex.ARSIZE] = 2**port['ario']['arsize'] * 8
        self.queue.append([port['ario']['arid'], port['ario']['araddr'], 0, 0, 0, 0, port['ario']['arlen'] + 1, 2**port['ario']['arsize'] * 8])
        self.arioRequest += 1
        port['ario']['arvalid'] = 0
        self.bundle.assign(port)
        # Read addr handle ok
        self.queue[-1][ReadIndex.ARIO] = 1
        return self.queue[-1]
    
    
    @driver_method()
    async def handleRio(self):
        debug_new = 1
        rid = 0
        port = {
                'rio': {
                    'rready': 1
                }
            }
        while True:
            if len(self.queue) == 0:
                port['rio']['rready'] = 0
                self.bundle.assign(port)
                await self.bundle.step(1)
                continue
            
            # Set delay here
            if self.rioDelay:
                await self.bundle.step(random.randint(1, self.rioDelay))
            
            port['rio']['rready'] = 1
            self.bundle.assign(port)
            # await self.bundle.step(1)
            await Value(self.bundle.rio.rvalid, 1)
            
            for item in self.queue:
                # if item[ReadIndex.ARID] == self.bundle.rio.rid.value and item[ReadIndex.ARIO] == 1 and item[ReadIndex.RIO] == 0:
                if item[ReadIndex.ARIO] == 1 and item[ReadIndex.RIO] == 0:
                
                    break       
            else:
                assert False, "R channel return unmatched rid"
            
            if item[ReadIndex.ARID] != self.bundle.rio.rid.value:
                print(self.bundle.rio.rid.value)
                self.dut.Finish()
                sys.exit(0)
            
            data = []
            # burst times
            length = item[ReadIndex.ARLEN]
            while True:
                if len(data) == length:
                    break
                if self.bundle.rio.rvalid.value:
                    data.append(self.bundle.rio.rdata.value)
                    if self.bundle.rio.rlast.value:
                        # assert len(data) == length, "Rlast finish recv data"
                        item[ReadIndex.RDATA] = mcparam.combine_data(data, item[ReadIndex.ARSIZE])
                        item[ReadIndex.RIO] = 1                       
                        # clear rready
                        # port['rio']['rready'] = 0  
                        assert item[ReadIndex.ARID] == self.bundle.rio.rid.value, "R channel rid not match"
                        break
                else:
                    await Value(self.bundle.rio.rvalid, 0)
                    continue
                
                self.bundle.assign(port)
                await self.bundle.step(1)

        
    
    async def Read(self, arid, araddr, arlen, arsize, arburst):
        port = {
            'ario': {
                'arid': arid,
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
        return await self.handleArio(port)

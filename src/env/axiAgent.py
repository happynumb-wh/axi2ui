from toffee import *
from utils import mcparam
from env.message import *
from env.axi2uiBundle import *
from env.axiIdAllocator import *
from env.scorebord import *
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
    def __init__(self, bundle: axiWriteBundle, refMemory:scoreBord, dut: DUTosmc_axi_top, idAllocator: axiIdAllocator):
        super().__init__(bundle)
        self.awioRequests = {}   # each id has a awioRequest
        self.finishRequests = {}   # each id has a finishRequest
        self.bundle = bundle
        self.message = axi2uiWriteMessage(bundle)
        self.refMemory = refMemory
        self.queues = {}   # each id has a queue
        self.awids = []   # AW channel ids, for W channel get corresponding awid
        self.dut = dut
        self.idAllocator = idAllocator
        self.wioDelay = 0
        self.wioRandomDelay = False
        self.awioDelay = 0
        self.awioRandomDelay = False
        self.bioDelay = 0
        self.bioRandomDelay = False
        self.waitForWready = 0
        self.dumpaddr = 0x0   # for debug

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
        
        awid = port['awio']['awid']
        if awid not in self.queues:
            self.queues[awid] = []
        
        for item in self.queues[awid]:
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
            self.queues[awid].append(item)
        
        if awid not in self.awioRequests:
            self.awioRequests[awid] = 0
        self.awioRequests[awid] += 1
        
        self.awids.append(awid)
        
        # set item[WriteIndex.WDATA] here and directly write refMemory
        data = []
        length = item[WriteIndex.WRLEN]
        while True:
            if len(data) == length:
                break
            if len(data) == length - 1:
                # last AXI data
                data.append(random.randint(0, 2**mcparam.AXI_DATAW - 1))
                item[WriteIndex.WDATA] = mcparam.combine_data(data, mcparam.AXI_DATAW)
            else:
                data.append(random.randint(0, 2**mcparam.AXI_DATAW - 1))
        
        port['awio']['awvalid'] = 0
        self.bundle.assign(port)
        
        self.refMemory.writeMemory(item[WriteIndex.ADDR], item[WriteIndex.WDATA])
        if item[WriteIndex.ADDR] == self.dumpaddr:
            print(f"axi refMemory write addr {hex(item[WriteIndex.ADDR])}, data {hex(item[WriteIndex.WDATA])}")
        
        # Write addr handle ok
        item[WriteIndex.AWIO] = 1
        # await self.bundle.step(1)
        return item
    
    @driver_method()
    async def handleWio(self):
        while True:            
            # get released awid
            if (len(self.awids) == 0):
                await self.bundle.step(1)
                continue
            awid = self.awids[0]
            # get corresponding queue and item
            item = None
            for q_item in self.queues[awid]:
                if q_item[WriteIndex.AWIO] == 1 and q_item[WriteIndex.WIO] == 0:
                    item = q_item
                    break
                if item is not None:
                    break
            
            if item is None:
                continue
           
            port = {
                'wio': {
                    'wuser': 0,
                    'wdata': 0,
                    'wstrb': 0,
                    'wlast': 0,
                    'wvalid': 0
                }
            }            
            
            data = mcparam.split_data(item[WriteIndex.WDATA], mcparam.AXI_DATAW)
            port['wio']['wvalid'] = 1
            port['wio']['wstrb'] = 0xffffffff
            port['wio']['wdata'] = data.pop(0)

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
            
            # only pop awids when w channel handshakes
            self.awids.pop(0)
            
            length = 1
            finish = False
            while True:
                if finish:
                    break
                if self.bundle.wio.wready.value:
                    if self.bundle.wio.wlast.value:
                        port['wio']['wlast'] = 0 
                        port['wio']['wvalid'] = 0
                        if length != item[WriteIndex.WRLEN]:
                            print("Wlast finish recv data (axi length error)")
                        item[WriteIndex.WDATA] = mcparam.combine_data(data, mcparam.AXI_DATAW)
                        item[WriteIndex.WIO] = 1
                        finish = True
                    else:
                        port['wio']['wdata'] = data.pop(0)
                        if len(data) == 0:
                            port['wio']['wlast'] = 1
                        length += 1
                else:
                    await Value(self.bundle.wio.wready, 1)
                    length += 1
                    continue

                self.bundle.assign(port)
                await self.bundle.step(1)

           
    @driver_method()
    async def handleBio(self):
        while True:
            if not any(self.queues.values()):
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
            
            # Find the item with matching bid
            item = None
            bid = self.bundle.bio.bid.value
            if bid in self.queues:
                for q_item in self.queues[bid]:
                    if q_item[WriteIndex.AWIO] == 1 and q_item[WriteIndex.WIO] == 1 and q_item[WriteIndex.BIO] == 0:
                        item = q_item
                        break
                        
            if item is None:
                print(f"B channel return unmatched bid {bid}, write queues: {self.queues}")
                self.dut.Finish()
                sys.exit(0)
            
            if item[WriteIndex.AWID] != bid:
                print(f"B channel return unmatched bid {bid}, expected {item[WriteIndex.AWID]}, write queues: {self.queues}")
                self.dut.Finish()
                sys.exit(0)
            
            item[WriteIndex.BIO] = 1
            self.idAllocator.releaseWriteId(item[WriteIndex.ADDR], item[WriteIndex.AWID])
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
    REFDATA = 8
    LENGTH = 9
    
class axiReadAgent(Agent):
    '''
    Agent for the read channel
    '''
    def __init__(self, bundle: axiReadBundle, refMemory: scoreBord, dut: DUTosmc_axi_top, idAllocator: axiIdAllocator):
        super().__init__(bundle)
        self.arioRequests = {}   # each id has a arioRequest
        self.finishRequests = {}   # each id has a finishRequest
        self.bundle = bundle
        self.message = axi2uiReadMessage(bundle)
        self.refMemory = refMemory
        self.queues = {}   # each id has a queue
        self.dut = dut
        self.idAllocator = idAllocator
        self.rioDelay = 0
        self.dumpaddr = 0x0   # for debug
        
    def setRioDelay(self, delay):
        self.rioDelay = delay
    
    @driver_method()
    async def handleArio(self, port: dict):
        '''
        Queue: [arid, addr, ario, rio, rdata, token, arlen, arsize, refdata]
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
        
        arid = port['ario']['arid']
        if arid not in self.queues:
            self.queues[arid] = []
        
        item = [0] * ReadIndex.LENGTH
        item[ReadIndex.ARID] = port['ario']['arid']
        item[ReadIndex.ADDR] = port['ario']['araddr']
        item[ReadIndex.ARLEN] = port['ario']['arlen'] + 1
        item[ReadIndex.ARSIZE] = 2**port['ario']['arsize'] * 8
        item[ReadIndex.REFDATA] = self.refMemory.readMemory(item[ReadIndex.ADDR])
        if item[ReadIndex.ADDR] == self.dumpaddr:
            print(f"axi refMemory read addr {hex(item[ReadIndex.ADDR])}, data {hex(item[ReadIndex.REFDATA])}")
        self.queues[arid].append(item)
        if arid not in self.arioRequests:
            self.arioRequests[arid] = 0
        self.arioRequests[arid] += 1
        port['ario']['arvalid'] = 0
        self.bundle.assign(port)
        # Read addr handle ok
        self.queues[arid][-1][ReadIndex.ARIO] = 1
        return self.queues[arid][-1]
    
    
    @driver_method()
    async def handleRio(self):
        port = {
                'rio': {
                    'rready': 1
                }
            }
        while True:
            if not any(self.queues.values()):
                port['rio']['rready'] = 0
                self.bundle.assign(port)
                await self.bundle.step(1)
                continue
            
            # Set delay here
            if self.rioDelay:
                await self.bundle.step(self.rioDelay)
            
            port['rio']['rready'] = 1
            self.bundle.assign(port)
            # await self.bundle.step(1)
            await Value(self.bundle.rio.rvalid, 1)
            
            rid = self.bundle.rio.rid.value
            item = None
            if rid in self.queues:
                for q_item in self.queues[rid]:
                    if q_item[ReadIndex.ARIO] == 1 and q_item[ReadIndex.RIO] == 0:
                        item = q_item
                        break
                        
            if item is None:
                print(f"R channel return unmatched rid {rid}, read queues: {self.queues}")
                self.dut.Finish()
                sys.exit(0)
            
            if item[ReadIndex.ARID] != self.bundle.rio.rid.value:
                print(f"handleRio: {self.bundle.rio.rid.value}")
                print(item[ReadIndex.ARID])
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
                        if item[ReadIndex.ARID] != self.bundle.rio.rid.value:
                            print("R channel rid not match")
                        self.idAllocator.releaseReadId(item[ReadIndex.ADDR], item[ReadIndex.ARID])
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

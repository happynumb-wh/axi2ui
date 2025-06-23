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
        self.uiReadAgent = uiReadAgent(uiBundle.readBundle, self.memory, self.readConsis)
        self.uiWriteAgent = uiWriteAgent(uiBundle.writeBundle, self.memory, self.writeConsis)
        self.dut = dut
        self.handler = []
        # commit switch defalut is 1
        self.deleteCommit = 1
        
        self.dut.io_apb_config_done.value = 1

    def readConsis(self, token: int):
        '''
        This function is used to check the read consistency, first commit ui should finish first
        '''
        # Read token
        rtoken = token & ~(0x1 << 9)
        rflag = token & 0x1 << 9
        
            # Read data
            # data = self.memory.read(item[0])
        for item in reversed(self.uiWriteAgent.queue):
            if item[1] == 1 and item[2] == 0:
                wtoken = item[-1] & ~(0x1 << 9)
                wflag =  item[-1] & 0x1 << 9
                if rflag == wflag:
                    # flag equal, smaller is older, wait it
                    if rtoken > wtoken:
                        return 1
                    else:
                        return 0
                    
                else:
                    # flag not equal, larger is older, wait it
                    if rtoken < wtoken:
                        return 1
                    else:
                        return 0
            else:
                return 0
        else:
            return 0                    
    
    def writeConsis(self, token: int):
        '''
        This function is used to check the write consistency, first commit axi should finish first
        '''
        # Write token
        wtoken = token & ~(0x1 << 9)
        wflag = token & 0x1 << 9
        for item in reversed(self.uiReadAgent.queue):
            if item[1] == 1 and item[2] == 0:
                rtoken = item[-1] & ~(0x1 << 9)
                rflag =  item[-1] & 0x1 << 9
                
                if rflag == wflag:
                    # flag equal, smaller is older, wait it
                    if wtoken > rtoken:
                        return 1
                    else:
                        return 0
                else:
                    # flag not equal, larger is older, wait it
                    if wtoken < rtoken:
                        return 1
                    else:
                        return 0
        else:
            return 0


    def judgeConsis(self, addr, axiqueue:list, uiqueue:list):
        '''
        Only support 512 bit data width
        '''
        addrBase = addr
        addrEnd = addr + UI_DATAW // 8
        countUI = sum([1 for i in uiqueue if i[1] == 1])
        countAXI = sum([1 for i in axiqueue if i[1] == 1])
        assert countUI <= countAXI, "UI request should less than AXI request"      
        for i in range(countUI - 1, countAXI):
            # AXI request is more than UI request
            axiAddrBase = axiqueue[i][0]
            axiAddrEnd = axiqueue[i][0] + UI_DATAW // 8
            # Address is overlap
            if addrBase >= axiAddrBase and addrBase <= axiAddrEnd or \
                addrEnd >= axiAddrBase and addrEnd <= axiAddrEnd:
                return 1                
        
        return 0

    async def consisCheck(self):
        while True:
            raddr = self.axiReadAgent.bundle.ario.araddr.value
            waddr = self.axiWriteAgent.bundle.awio.awaddr.value
            rconsit = self.dut.osmc_axi_top_u_axi_consis_io_consis_io_rconsis.value
            wconsit = self.dut.osmc_axi_top_u_axi_consis_io_consis_io_wconsis.value
            
            assert rconsit == self.judgeConsis(raddr, self.axiWriteAgent.queue, self.uiWriteAgent.queue), \
                "Read consis signal not match"
            assert wconsit == self.judgeConsis(waddr, self.axiReadAgent.queue, self.uiReadAgent.queue), \
                "Write consis signal not match"
            
            await self.readBundle.step(1)
    
    
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
        self.handler.append(toffee.create_task(self.consisCheck()))
        
        
    
    
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
            
            if self.axiReadAgent.finishRequest >= self.axiReadAgent.arioRequest:
                await self.readBundle.step(1)
                continue
            
            if self.deleteCommit:
                idx = 0
            else:
                idx = self.axiReadAgent.finishRequest
                if idx >= len(self.uiReadAgent.queue):
                    await self.readBundle.step(1)
                    continue
            axiItem = self.axiReadAgent.queue[idx]
            uiItem = self.uiReadAgent.queue[idx]
            
            if axiItem[2] and axiItem[1] and uiItem[1] and uiItem[2]:
                assert axiItem[0] == uiItem[0], "Read address not match"
                if axiItem[3] != uiItem[3]:
                    print(f"Read data not match: addr: {hex(axiItem[0])} Token: {hex(axiItem[5])}, idx: {self.axiReadAgent.finishRequest}")
                    print(f"axi: {hex(axiItem[3])} ui: {hex(uiItem[3])}")
                    self.dut.Finish()
                    exit(0)
                self.axiReadAgent.finishRequest += 1
                if self.deleteCommit:
                    self.axiReadAgent.queue.pop(idx)
                    self.uiReadAgent.queue.pop(idx)
                    
            await self.readBundle.step(1)
            
    async def writeCommit(self):
        while True:
            if len(self.axiWriteAgent.queue) == 0 or len(self.uiWriteAgent.queue) == 0:
                await self.writeBundle.step(1)
                continue
            
            if self.axiWriteAgent.finishRequest >= self.axiWriteAgent.awioRequest:
                await self.writeBundle.step(1)
                continue
            
            if self.deleteCommit:
                idx = 0
            else:
                idx = self.axiWriteAgent.finishRequest
                if idx >= len(self.uiWriteAgent.queue):
                    await self.writeBundle.step(1)
                    continue
            axiItem = self.axiWriteAgent.queue[idx]
            uiItem = self.uiWriteAgent.queue[idx]
            
            if axiItem[3] and axiItem[2] and axiItem[1] and uiItem[1] and uiItem[2]:
                assert axiItem[0] == uiItem[0], "Write address not match"
                if axiItem[4] != uiItem[3]:
                    print(f"Write data not match: addr: {hex(axiItem[0])}, idx: f{self.axiWriteAgent.finishRequest}")
                    print(f"axi: {hex(axiItem[4])} ui: {hex(uiItem[3])}")
                    self.dut.Finish()
                    exit(0)
                self.axiWriteAgent.finishRequest += 1
                if self.deleteCommit:
                    self.axiWriteAgent.queue.pop(idx)
                    self.uiWriteAgent.queue.pop(idx)
            await self.writeBundle.step(1)
                 
    async def Finish(self):
        while True:
            if self.axiReadAgent.finishRequest == self.axiReadAgent.arioRequest and self.axiWriteAgent.finishRequest == self.axiWriteAgent.awioRequest:
                break
            await ClockCycles(self.dut, 1)
        print("Finish")
        for task in self.handler:
            task.cancel()
    
    def __del__(self):
        self.dut.Finish()
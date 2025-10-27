from toffee import *
from env.axi2uiBundle import *
from env.message import *
from env.axiAgent import *
from env.uiAgent import *
from env.axiIdAllocator import *
from axi2ui import *
import toffee
import sys
import os
import tqdm

class axi2uiEnv(Env):
    def __init__(self, axiBundle: axiMasterBundle, uiBundle: uiSlaveBundle, dut: DUTosmc_axi_top):
        super().__init__()
        self.readBundle = axiBundle.readBundle
        self.writeBundle = axiBundle.writeBundle
        self.memory = scoreBord()   # ui use this memory
        self.refMemory = scoreBord()   # checkTrace use this memory
        self.axiIdAllocator = axiIdAllocator(14)
        self.axiReadAgent = axiReadAgent(axiBundle.readBundle, self.refMemory, dut, self.axiIdAllocator)
        self.axiWriteAgent = axiWriteAgent(axiBundle.writeBundle, self.refMemory, dut, self.axiIdAllocator)
        self.uiReadAgent = uiReadAgent(uiBundle.readBundle, self.memory, self.readConsis)
        self.uiWriteAgent = uiWriteAgent(uiBundle.writeBundle, self.memory, self.writeConsis)
        self.dut = dut
        self.handler = []
        self.checkQueues = {}   # each id has a checkQueue
        # commit switch defalut is 1
        self.deleteCommit = 1
        self.dumpaddr = 0x2f17f6700   # for debug
        self.axiReadAgent.dumpaddr = self.dumpaddr   # for debug
        self.axiWriteAgent.dumpaddr = self.dumpaddr   # for debug
        self.uiReadAgent.dumpaddr = self.dumpaddr   # for debug
        self.uiWriteAgent.dumpaddr = self.dumpaddr   # for debug
        
        self.dut.io_apb_config_done.value = 1

    def backDoorWrite(self, tfile: str):
        print("Back door writing...")
        with open(tfile, "r") as f:
            lines = f.readlines()
            full_times = len(lines)
            f.seek(0, os.SEEK_SET)
            for tqdm_lines in tqdm.tqdm(range(full_times)):
                line = lines[tqdm_lines]
                if "R" in line or "W" in line:
                    addr = int(line.split(" ")[-1], 16)
                    data = random.randint(0, 2**512 - 1)   # 1 cacheline -> 64 Byte -> 512 bit
                    self.memory.writeMemory(addr, data)
                    self.refMemory.writeMemory(addr, data)
                    if addr == self.dumpaddr:
                        print(f"Back door write addr {hex(addr)}, data {hex(data)}")
                else:
                    print("Error: Unknow command")
                    self.dut.Finish()
                    exit(0)
        print("Back door write done!")
    
    def readConsis(self, addr):
        '''
        This function is used to check the read consistency, first commit ui (with the same addr) should finish first
        '''
        # readConsis only check the same addr
        # only support deleteCommit == 1
        for item in self.uiWriteAgent.queue:
            if item[0] == addr and item[1] == 1 and item[2] == 0:
                return True
        return False

    
    def writeConsis(self, addr):
        '''
        This function is used to check the write consistency, first commit ui (with the same addr) should finish first
        '''
        # TODO: writeConsis only check the same addr
        # only support deleteCommit == 1
        for item in self.uiReadAgent.queue:
            if item[0] == addr and item[1] == 1 and item[2] == 0:
                return True
        return False

    def judgeConsis(self, addr, axiqueues:dict, uiqueue:list):
        '''
        Only support 512 bit data width
        '''
        addrBase = addr
        addrEnd = addr + UI_DATAW // 8
        countUI = sum([1 for i in uiqueue if i[1] == 1])
        countAXI = sum([1 for queue in axiqueues.values() for i in queue if i[1] == 1])
        if countUI > countAXI:
            print("UI request should less than AXI request")
            self.dut.Finish()
            exit(0)
        
        # TODO: Check all AXI queues for address overlap
        pass
                
        # for i in range(countUI - 1, countAXI):
        #     # AXI request is more than UI request
        #     axiAddrBase = axiqueue[i][1]
        #     axiAddrEnd = axiqueue[i][1] + UI_DATAW // 8
        #     # Address is overlap
        #     if addrBase >= axiAddrBase and addrBase <= axiAddrEnd or \
        #         addrEnd >= axiAddrBase and addrEnd <= axiAddrEnd:
        #         return 1                
        
        # return 0

    async def consisCheck(self):
        while True:
            raddr = self.axiReadAgent.bundle.ario.araddr.value
            waddr = self.axiWriteAgent.bundle.awio.awaddr.value
            
            # TODO: consis check, WARNING: assert not work
            # rconsit = self.dut.osmc_axi_top_u_axi_consis_io_consis_io_rconsis.value
            # wconsit = self.dut.osmc_axi_top_u_axi_consis_io_consis_io_wconsis.value
            
            # assert rconsit == self.judgeConsis(raddr, self.axiWriteAgent.queues, self.uiWriteAgent.queue), \
            #     "Read consis signal not match"
            # assert wconsit == self.judgeConsis(waddr, self.axiReadAgent.queues, self.uiReadAgent.queue), \
            #     "Write consis signal not match"
            
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
        self.handler.append(toffee.create_task(self.checkTrace()))
        self.handler.append(toffee.create_task(self.consisCheck()))
        
        
    
    
    async def reset(self):
        self.dut.reset.value = 1
        await self.readBundle.step(100)
        self.dut.reset.value = 0
        await self.readBundle.step(10)

    
    
    async def readCommit(self):
        # TODO: we don't check uiItem because it is not easy to match uiItem with axiItem in the case of virtualChannel on,
        #       so just delete queue of uiAgent
        while True:
            if all(len(queue) == 0 for queue in self.axiReadAgent.queues.values()):
                await self.readBundle.step(1)
                continue
            
            all_finished = all(
                self.axiReadAgent.finishRequests.get(id, 0) >= self.axiReadAgent.arioRequests.get(id, 0)
                for id in self.axiReadAgent.queues.keys()
            )
            if all_finished:
                await self.readBundle.step(1)
                continue
            
            for id, queue in self.axiReadAgent.queues.items():
                if len(queue) == 0:
                    continue
            
                axiItem = queue[0]
                if axiItem[ReadIndex.ARIO] and axiItem[ReadIndex.RIO]:                  
                    self.axiReadAgent.finishRequests[id] = self.axiReadAgent.finishRequests.get(id, 0) + 1
                    # print(f"[debug]: READ ID {id}, readCommit finish {self.axiReadAgent.finishRequests[id]} of {self.axiReadAgent.arioRequests[id]} requests")
                    queue.pop(0)

            await self.readBundle.step(1)
            
    async def writeCommit(self):
        # TODO: we don't check uiItem because it is not easy to match uiItem with axiItem in the case of virtualChannel on,
        #       so just delete queue of uiAgent
        while True:
            if all(len(queue) == 0 for queue in self.axiWriteAgent.queues.values()):
                await self.writeBundle.step(1)
                continue
            
            all_finished = all(
                self.axiWriteAgent.finishRequests.get(id, 0) >= self.axiWriteAgent.awioRequests.get(id, 0)
                for id in self.axiWriteAgent.queues.keys()
            )
            if all_finished:
                await self.writeBundle.step(1)
                continue
            
            for id, queue in self.axiWriteAgent.queues.items():
                if len(queue) == 0:
                    continue
                
                axiItem = queue[0]
                if axiItem[WriteIndex.AWIO] and axiItem[WriteIndex.WIO] and axiItem[WriteIndex.BIO]:
                    self.axiWriteAgent.finishRequests[id] = self.axiWriteAgent.finishRequests.get(id, 0) + 1
                    # print(f"[debug]: WRITE ID {id}, writeCommit finish {self.axiWriteAgent.finishRequests[id]} of {self.axiWriteAgent.awioRequests[id]} requests")
                    queue.pop(0)
            
            await self.writeBundle.step(1)

    async def checkTrace(self):
        while True:
            for id, queue in self.checkQueues.items():
                if len(queue) == 0:
                    continue
                # TODO: NOTICE: only support deleteCommit == 1
                item = queue[0]
                if item[0] == 'R':
                    axiItem = item[1]
                    if axiItem[ReadIndex.ARIO] and axiItem[ReadIndex.RIO]:
                        if axiItem[ReadIndex.RDATA] != axiItem[ReadIndex.REFDATA]:
                            print(f"[Error]: Data not match in {hex(axiItem[ReadIndex.ADDR]) } expect {hex(axiItem[ReadIndex.REFDATA])} but got {hex(axiItem[ReadIndex.RDATA])}")
                            self.dut.Finish()
                            exit(0)
                        print(f"[debug]: READ ID {id}, checkTrace finish addr {hex(axiItem[ReadIndex.ADDR])} data {hex(axiItem[ReadIndex.RDATA])}")
                        queue.pop(0)
                elif item [0] == 'W':
                    axiItem = item[1]
                    if axiItem[WriteIndex.AWIO] and axiItem[WriteIndex.WIO] and axiItem[WriteIndex.BIO]:
                        queue.pop(0)
            
            await ClockCycles(self.dut, 1)
                 
    async def Finish(self):
        while True:
            read_all_finished = all(
                self.axiReadAgent.finishRequests.get(id, 0) >= self.axiReadAgent.arioRequests.get(id, 0)
                for id in self.axiReadAgent.queues.keys()
            )
            write_all_finished = all(
                self.axiWriteAgent.finishRequests.get(id, 0) >= self.axiWriteAgent.awioRequests.get(id, 0)
                for id in self.axiWriteAgent.queues.keys()
            )
            check_queues_all_finished = all(
                len(queue) == 0
                for id, queue in self.checkQueues.items()
            )
            if read_all_finished and write_all_finished and check_queues_all_finished:
                break
            
            await ClockCycles(self.dut, 1)
        print("Finish")
        for task in self.handler:
            task.cancel()
    
    def __del__(self):
        self.dut.Finish()
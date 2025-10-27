#!/bin/python
from axi2ui import *
from env.axi2uiBundle import *
from env.axi2uiEnv import *
from toffee.triggers import *
from utils import mcparam
import toffee
import sys
import os
import tqdm
import traceback
import asyncio


async def test_top(dut: DUTosmc_axi_top, tfile:str):
    toffee.start_clock(dut)
    # axi bundle
    axiBundle = axiMasterBundle()
    axiBundle.bind(dut)
    axiBundle.set_all(0)
    
    # ui bundle
    uiBundle = uiSlaveBundle()
    uiBundle.bind(dut)
    uiBundle.set_all(0)
    
    axiBundle.reset.value = 1
    
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    
    ###############################################################
    axiEnv = axi2uiEnv(axiBundle, uiBundle, dut)
    await axiEnv.reset()
    toffee.create_task(axiEnv.envDeamon())
    
    
    # axiEnv.uiReadAgent.setRioRandom(1)
    axiEnv.uiReadAgent.setRioDelay(10)
    # axiEnv.uiWriteAgent.setWioDelay(100)
    # axiEnv.axiReadAgent.setRioDelay(20)
    # axiEnv.axiWriteAgent.setWioDelay(20)
    
    # print("waiting...")
    # for i in range(10):
    #     await axiEnv.readBundle.step(100000)
    #     print(f"{i}")
    # # print("waiting done")
    # arid = -1
    # for i in range(1000):
    #     arid = (arid + 1) % (1 << mcparam.AXI_IDW)
    #     await axiEnv.axiReadAgent.Read(arid, 0x1000 + i * 0x100, burst_length - 1, 0x5, 0x2)
    #     await axiEnv.readBundle.step(random.randint(0, 1000))
    #     print(i)
    
    axiEnv.backDoorWrite(tfile)
    with open(tfile, "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        # latencies = [5-1, 9-1, 1-1, 10-1]
        for tqdm_lines in tqdm.tqdm(range(full_times)):
            line = lines[tqdm_lines]
            if "R" in line:
                addr = int(line.split(" ")[-1], 16)
                arid = axiEnv.axiIdAllocator.allocReadId(addr)
                # try:
                    # continue
                item = await axiEnv.axiReadAgent.Read(arid, addr, 1, 0x5, 0x2)
                axiEnv.checkQueues.setdefault(arid, []).append(['R', item])
                # if tqdm_lines < len(latencies):
                #     await axiEnv.readBundle.step(latencies[tqdm_lines])
                # except asyncio.TimeoutError:
                #     assert False, 'Timeout: read %s, uiReadAgent queue lenth: %d' % (addr, len(axiEnv.uiReadAgent.queue))
                
            elif "W" in line:
                addr = int(line.split(" ")[-1], 16)
                awid = axiEnv.axiIdAllocator.allocWriteId(addr)
                # try:
                    # continue
                item = await axiEnv.axiWriteAgent.Write(awid, addr, 1, 0x5, 0x2)
                axiEnv.checkQueues.setdefault(awid, []).append(['W', item])
                # except asyncio.TimeoutError:
                #     assert False, (
                #         f'Timeout: write 0x{addr}\n'
                #         f'  uiWriteAgent queue length: {len(axiEnv.uiWriteAgent.queue)}\n'
                #         f'  uiReadAgent queue length: {len(axiEnv.uiReadAgent.queue)}\n'
                #         f'  Write consis result: {axiEnv.uiWriteAgent.debug_writeConsisResult}\n'
                #         f'  Addr: 0x{axiEnv.uiWriteAgent.debug_writeConsisAddr:x}\n'
                #         f'  Token: 0x{axiEnv.uiWriteAgent.debug_writeConsisToken:x}\n'
                #         # f'  uiReadAgent queue: {", ".join(f"{item}" for item in axiEnv.uiReadAgent.queue)}'
                #     )
            else:
                print("Error: Unknow command")
                dut.Finish()
                exit(0)
    
    # await axiEnv.Finish()
    try:
        await asyncio.wait_for(axiEnv.Finish(), timeout=10)
    except asyncio.TimeoutError:
        assert False, (
            f'axiEnv.Finish Timeout:\n'
            f'axiReadAgent.finishRequests: {axiEnv.axiReadAgent.finishRequests}\n'
            f'axiReadAgent.arioRequests: {axiEnv.axiReadAgent.arioRequests}\n'
            f'axiWriteAgent.finishRequests: {axiEnv.axiWriteAgent.finishRequests}\n'
            f'axiWriteAgent.awioRequests: {axiEnv.axiWriteAgent.awioRequests}\n'
        )



if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f'Trace file {sys.argv[1]}')
    else:
        print("No trace file")
        exit(1)
    toffee.setup_logging(toffee.WARNING)
    
    # dut = DUTosmc_axi_top()
    # 仅vcs时, 向DUTosmc_axi_top传参
    cov_dir = os.path.join(os.getcwd(), "cov")
    try:
        dut = DUTosmc_axi_top(["-cm", "line+cond+fsm+tgl",
                               "-cm_name", "simv",
                               "-cm_dir", cov_dir])
    except Exception as e:
        print(f"Exception in create_dut: {e}")
        traceback.print_exc()
    
    dut.InitClock("clock")
    
    dut.reset.AsImmWrite()
        
    toffee.run(test_top(dut, sys.argv[1]))
    dut.Finish()


    
    
    
    
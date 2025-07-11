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
    # axiEnv.uiReadAgent.setRioDelay(100)
    # axiEnv.uiWriteAgent.setWioDelay(100)
    # axiEnv.axiReadAgent.setRioDelay(20)
    # axiEnv.axiWriteAgent.setWioDelay(20)
    
    # print("waiting...")
    # for i in range(10):
    #     await axiEnv.readBundle.step(100000)
    #     print(f"{i}")
    # print("waiting done")
    
    with open(tfile, "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        arid = -1
        awid = -1
        for tqdm_lines in tqdm.tqdm(range(full_times // 1000)):
            line = lines[tqdm_lines]
            if "R" in line:
                arid = (arid + 1) % (1 << mcparam.AXI_IDW)
                addr = line.split(" ")[-1]
                # try:
                    # continue
                await axiEnv.axiReadAgent.Read(arid, int(addr, 16), 1, 0x5, 0x2)
                # except asyncio.TimeoutError:
                #     assert False, 'Timeout: read %s, uiReadAgent queue lenth: %d' % (addr, len(axiEnv.uiReadAgent.queue))
                
            elif "W" in line:
                awid = (awid + 1) % (1 << mcparam.AXI_IDW)
                addr = line.split(" ")[-1]
                # try:
                    # continue
                await axiEnv.axiWriteAgent.Write(awid, int(addr, 16), 1, 0x5, 0x2)
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
    
    await axiEnv.Finish()



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


    
    
    
    
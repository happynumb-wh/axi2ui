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
    
    await axiBundle.step(100)
    axiBundle.reset.value = 0
    await axiBundle.step(10)
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    
    ###############################################################
    axiEnv = axi2uiEnv(axiBundle, uiBundle, dut)
    toffee.create_task(axiEnv.envDeamon())
    
    
    # print('Write')
    
    # for i in range(36):
    #     await axiEnv.axiWriteAgent.Write(0x100000 + 0x100 * i, burst_length - 1, 0x5, 0x2)
    with open(tfile, "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        for tqdm_lines in tqdm.tqdm(range(full_times)):
            line = lines[tqdm_lines]
            if "R" in line:
                id, time, type, addr = line.split(" ")
                await axiEnv.axiReadAgent.Read(int(addr, 16), burst_length - 1, 0x5, 0x2)
                
            elif "W" in line:
                id, time, type, addr = line.split(" ")
                await axiEnv.axiWriteAgent.Write(int(addr, 16), burst_length - 1, 0x5, 0x2)
            else:
                print("Error: Unknow command")
                dut.Finish()
                exit(0)

    # axiEnv.uiReadAgent.setRioDelay(200)
    # for i in range(128):
    #     await axiEnv.axiReadAgent.Read(0x1000 + 0x100 * i, burst_length - 1, 0x5, 0x2)
    # Wait all finished
    await axiEnv.Finish()
    # await ClockCycles(dut, 200000)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f'Trace file {sys.argv[1]}')
    else:
        print("No trace file")
        exit(1)
    toffee.setup_logging(toffee.WARNING)
    dut = DUTosmc_axi_top()
    dut.InitClock("clock")
    
    dut.reset.AsImmWrite()
        
    toffee.run(test_top(dut, sys.argv[1]))
    dut.Finish()


    
    
    
    
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
    
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    
    ###############################################################
    axiEnv = axi2uiEnv(axiBundle, uiBundle, dut)
    await axiEnv.reset()
    toffee.create_task(axiEnv.envDeamon())
    
    
    axiEnv.uiReadAgent.setRioRandom(1)
    
    with open(tfile, "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        for tqdm_lines in tqdm.tqdm(range(full_times // 10)):
            line = lines[tqdm_lines]
            if "R" in line:
                addr = line.split(" ")[-1]
                await axiEnv.axiReadAgent.Read(int(addr, 16), burst_length - 1, 0x5, 0x2)
                
            elif "W" in line:
                addr = line.split(" ")[-1]
                await axiEnv.axiWriteAgent.Write(int(addr, 16), burst_length - 1, 0x5, 0x2)
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
    dut = DUTosmc_axi_top()
    dut.InitClock("clock")
    
    dut.reset.AsImmWrite()
        
    toffee.run(test_top(dut, sys.argv[1]))
    dut.Finish()


    
    
    
    
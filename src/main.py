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
    axiEnv.uiReadAgent.setRioDelay(100)
    # axiEnv.uiWriteAgent.setWioDelay(100)
    # axiEnv.axiReadAgent.setRioDelay(20)
    # axiEnv.axiWriteAgent.setWioDelay(20)
    
    with open(tfile, "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        for tqdm_lines in tqdm.tqdm(range(full_times // 100)):
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
    
    # dut = DUTosmc_axi_top()
    # 仅vcs时, 向DUTosmc_axi_top传参
    cov_dir = os.path.join(os.getcwd(), "cov")
    try:
        # dut = DUTmc_wrapper(f"+trace_file={sys.argv[1]}")
        dut = DUTosmc_axi_top([f"+trace_file={sys.argv[1]}",
                             "-cm", "line+cond+fsm+tgl",
                             "-cm_name", "simv",
                             "-cm_dir", cov_dir])
    except Exception as e:
        print(f"Exception in create_dut: {e}")
        traceback.print_exc()
    
    dut.InitClock("clock")
    
    dut.reset.AsImmWrite()
        
    toffee.run(test_top(dut, sys.argv[1]))
    dut.Finish()


    
    
    
    
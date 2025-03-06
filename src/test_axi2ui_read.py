#!/bin/python
from axi2ui import *
from env.axi2uiBundle import *
from env.axi2uiEnv import *
from toffee.triggers import *
from utils import mcparam
import toffee_test
import toffee
import sys
import os
import tqdm


"""
Sequence Read test
"""
@toffee_test.testcase
async def test_axi2uiSequenceWrite(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = 0x10000000
    # axi2ui_Env.uiWriteAgent.setWioDelay(50)
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_token_fifo_vaild_data.value))
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_cmd_fifo_vaild_data.value))
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, 0x5, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
Random Read test
"""
@toffee_test.testcase
async def test_axi2uiRandomWrite(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()

"""

"""
@toffee_test.testcase
async def test_axi2uiTrace(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    with open('./test/data/trace2/bzip2_liberty_0_rand500w.txt', "r") as f:
        lines = f.readlines()
        full_times = len(lines)
        f.seek(0, os.SEEK_SET)
        for tqdm_lines in tqdm.tqdm(range(full_times//1000)):
            # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_token_fifo_vaild_data.value))
            # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_cmd_fifo_vaild_data.value))
            line = lines[tqdm_lines]
            if "R" in line:
                addr = line.split(" ")[-1]
                await axi2ui_Env.axiReadAgent.Read(int(addr, 16), 1, 0x5, 0x2)
                
            elif "W" in line:
                addr = line.split(" ")[-1]
                await axi2ui_Env.axiWriteAgent.Write(int(addr, 16), 1, 0x5, 0x2)
            else:
                print("Error: Unknow command")
                dut.Finish()
                exit(0)
    await axi2ui_Env.Finish()
    
    
"""
Sequence Read test
"""
@toffee_test.testcase
async def test_axi2uiSequenceRead(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = 0x10000000
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_token_fifo_vaild_data.value))
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_cmd_fifo_vaild_data.value))
        await axi2ui_Env.axiReadAgent.Read(addr, burst_length - 1, 0x5, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
Random Read test
"""
@toffee_test.testcase
async def test_axi2uiRandomRead(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_token_fifo_vaild_data.value))
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_cmd_fifo_vaild_data.value))
        await axi2ui_Env.axiReadAgent.Read(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()

"""
Random Read test
"""
@toffee_test.testcase
async def test_axi2uiRROB(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    axi2ui_Env.uiReadAgent.setRioRandom(1)
    axi2ui_Env.uiReadAgent.setRioDelay(100)
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = 0x10000000
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        # print(axi2ui_Env.dut.osmc_axi_top__u_axi_read_io_ready_stall.value)
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_token_fifo_vaild_data.value))
        # print(hex(axi2ui_Env.dut.osmc_axi_top_u_axi_read_u_axi_r_cmdbuffer_cmd_fifo_vaild_data.value))
        
        await axi2ui_Env.axiReadAgent.Read(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()



"""
Coverage definition
"""

import toffee.funcov as fc
from toffee.funcov import CovGroup


def adder_cover_point(axi2ui: DUTosmc_axi_top):
    g = CovGroup("DUTosmc_axi_top addition function")

    g.add_cover_point(axi2ui.osmc_axi_top__u_axi_read_io_ready_stall, {"io_ready_stall is 1": fc.Eq(1)}, name="io_ready_stall set 1")

    return g


@toffee_test.fixture
async def axi2ui_Env(toffee_request: toffee_test.ToffeeRequest):
    toffee.setup_logging(toffee.WARNING)
    dut = toffee_request.create_dut(DUTosmc_axi_top)
    toffee.start_clock(dut)
    toffee_request.add_cov_groups(adder_cover_point(dut))
    dut.InitClock("clock")
    # axi bundle
    axiBundle = axiMasterBundle()
    axiBundle.bind(dut)
    axiBundle.set_all(0)
    
    # ui bundle
    uiBundle = uiSlaveBundle()
    uiBundle.bind(dut)
    uiBundle.set_all(0)
    
    return axi2uiEnv(axiBundle, uiBundle, dut)



    
    
    
    
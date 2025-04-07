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
# Read item
# [addr, ario, rio, rdata, token, arlen, arsize]

# Write item
# [addr, awio, wio, bio, wdata, token, wrlen, wrsize]


"""
Random Write test
"""
@toffee_test.testcase
async def test_axi2uiWriteConsis(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = 0x10000000
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    axi2ui_Env.deleteCommit = False # save finish request
    axi2ui_Env.axiReadAgent.setRioDelay(1000) # delay read response to raise wconsis easily
    
    ##############################################################################
    # for i in range(3):
    target_addr = addr + 0x40 * 13
    # First write a random data to target addr
    preRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
    for i in range(16):
        item =  await axi2ui_Env.axiReadAgent.Read(addr, burst_length - 1, 0x5, 0x2)
        if addr == target_addr:
            middleRequest = item
        addr += 0x40 # for 512bit data
    ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
    FinalRequest =  await axi2ui_Env.axiReadAgent.Read(target_addr, burst_length - 1, 0x5, 0x2)
    
    await axi2ui_Env.Finish()
    
    # Check write data is same as read data
    assert preRequest[4] == middleRequest[3], "Middle data not match"
    assert middleRequest[3] != FinalRequest[3], "Error: Final data should not match"
    assert ThirdRequest[4] == FinalRequest[3], "Final data not match"
    


"""
Read Consis test
"""
@toffee_test.testcase
async def test_axi2uiConsis(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    axi2ui_Env.deleteCommit = False # save finish request
    # axi2ui_Env.axiReadAgent.setRioDelay(1000) # delay read response to raise wconsis easily
    
    ##############################################################################
    # RAW test, delay write response to raise rconsis easily
    axi2ui_Env.uiWriteAgent.setWioDelay(1000)
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiReadAgent.Read(target_addr, burst_length - 1, 0x5, 0x2)
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiReadAgent.Read(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x20 # for 256bit data, Write requests have overlap addr
        ThirdRequest =  await axi2ui_Env.axiReadAgent.Read(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
        
    # WAR test, delay read response to raise wconsis easily
    axi2ui_Env.uiWriteAgent.setWioDelay(0)
    axi2ui_Env.uiReadAgent.setRioDelay(1000)
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiReadAgent.Read(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiReadAgent.Read(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiReadAgent.Read(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x20 # for 256bit data, read requests have overlap addr
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
        
    # WAW test, delay write response to raise wconsis easily
    axi2ui_Env.uiWriteAgent.setWioDelay(100)
    axi2ui_Env.uiReadAgent.setRioDelay(0)
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x40 # for 512bit data
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
    
    addr = 0x10000000
    for j in range (4):
        target_addr = addr + 0x40 * 13
        offset = 0
        for _ in range(16 << j):
            item =  await axi2ui_Env.axiWriteAgent.Write(addr + offset, burst_length - 1, 0x5, 0x2)
            # if addr == target_addr:
            #     middleRequest = item
            offset += 0x20 # for 256bit data, read requests have overlap addr
        ThirdRequest =  await axi2ui_Env.axiWriteAgent.Write(target_addr, burst_length - 1, 0x5, 0x2)
        addr += 0x4000   # we move test addr further
    
    await axi2ui_Env.Finish()



import toffee.funcov as fc
from toffee.funcov import CovGroup
def adder_cover_point(axi2ui: DUTosmc_axi_top):
    g = CovGroup("axi2ui consist function")

    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_consis_io_consis_io_wconsis, {"io_wconsis is 1": fc.Eq(1)}, name="io_wconsis set 1")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_consis_io_consis_io_wconsis, {"io_wconsis is 0": fc.Eq(1)}, name="io_wconsis set 0")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_consis_io_consis_io_rconsis, {"io_rconsis is 1": fc.Eq(1)}, name="io_rconsis set 1")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_consis_io_consis_io_rconsis, {"io_rconsis is 0": fc.Eq(1)}, name="io_rconsis set 0")
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
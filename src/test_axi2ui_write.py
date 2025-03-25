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
Sequence Write test
"""
@toffee_test.testcase
async def test_axi2uiSequenceWrite(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()

    # axi2ui_Env.axiWriteAgent.setWioDelay(100)
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = 0x10000000
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, 0x5, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
Random Write test
"""
@toffee_test.testcase
async def test_axi2uiRandomWrite(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    # axi2ui_Env.axiWriteAgent.setWioDelay(100)
    toffee.create_task(axi2ui_Env.envDeamon())
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in range(8192):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
axi awio: awready signal test
"""
@toffee_test.testcase
async def test_axi_awready(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    
    # awready is set 1 before awvalid
    axi2ui_Env.axiWriteAgent.setAwioDelay(1000)   # let axi delay response to make awready 1 and awvalid 0 easily
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        # await Value(axi2ui_Env.axiWriteAgent.bundle.awio.awready, 1)   # this may cause deadlock, we test it anyhow
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    # awready is set 1 after awvalid
    axi2ui_Env.axiWriteAgent.setAwioDelay(0)
    axi2ui_Env.uiWriteAgent.setAwioDelay(1000)   # let ui delay response to make awready 0 and awvalid 1 easily
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    # awready and awvalid is set 1 at the same cycle
    axi2ui_Env.axiWriteAgent.setAwioDelay(0)
    axi2ui_Env.uiWriteAgent.setAwioDelay(0)
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(8192):
        await Value(axi2ui_Env.axiWriteAgent.bundle.awio.awready, 1, 0)   # this may cause deadlock, we test it anyhow
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
axi wio: wready signal test
"""
@toffee_test.testcase
async def test_axi_wready(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    
    # wready and wvalid is set 1 at the same cycle
    axi2ui_Env.axiWriteAgent.setWioDelay(0)
    axi2ui_Env.uiWriteAgent.setWioDelay(1000)   # let axi delay response to make fifo full, so that wready 0
    axi2ui_Env.axiWriteAgent.setWaitForWready(True)
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    # wready is set 1 before wvalid
    axi2ui_Env.axiWriteAgent.setWioDelay(1000)   # let axi delay response to make wready 1 and wvalid 0 easily
    axi2ui_Env.uiWriteAgent.setWioDelay(0)
    axi2ui_Env.axiWriteAgent.setWaitForWready(False)
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        # await Value(axi2ui_Env.axiWriteAgent.bundle.wio.wready, 1)   # this may cause deadlock, we test it anyhow
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    # wready is set 1 after wvalid
    axi2ui_Env.axiWriteAgent.setWioDelay(0)
    axi2ui_Env.uiWriteAgent.setWioDelay(1000)   # let ui delay response to make wready 0 and wvalid 1 easily
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


"""
axi bio: bvalid signal test
"""
@toffee_test.testcase
async def test_axi_bvalid(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    
      # bvalid is set 1 before bready
    axi2ui_Env.axiWriteAgent.setBioDelay(1000)   # let axi delay response to make bvalid 1 and bready 0 easily
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        # await Value(axi2ui_Env.axiWriteAgent.bundle.awio.wready, 1)   # this may cause deadlock, we test it anyhow
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    # bvalid and bready is set 1 at the same cycle
    axi2ui_Env.axiWriteAgent.setBioDelay(0)
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        await Value(axi2ui_Env.axiWriteAgent.bundle.bio.bvalid, 1, 0)   # this may cause deadlock, we test it anyhow
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()


# all ui_* cover points are covered during test_axi_* except ui_awvalid_with_awready,
# so we test it lonely
    
"""
ui awio: awvalid signal test
"""
@toffee_test.testcase
async def test_ui_awvalid(axi2ui_Env: axi2uiEnv):
    await axi2ui_Env.reset()
    
    toffee.create_task(axi2ui_Env.envDeamon())
    
    # awvalid and awready is set 1 at the same cycle
    axi2ui_Env.axiWriteAgent.setAwioDelay(1000)   # let axi delay response to make ui_awvalid 0 easily
    axi2ui_Env.uiWriteAgent.setWaitForAwvalid(True)
    addr = random.randint(0x10000000, 2**mcparam.AXI_ADDRW - 1) & 0xFFFFFFFFFFFFFFc0
    burst_length = mcparam.UI_DATAW // mcparam.AXI_DATAW
    for i in tqdm.trange(1024):
        await axi2ui_Env.axiWriteAgent.Write(addr, burst_length - 1, BURST32, 0x2)
        addr += 0x100
    
    await axi2ui_Env.Finish()



"""
Coverage definition
"""

import toffee.funcov as fc
from toffee.funcov import CovGroup


def adder_cover_point(axi2ui: DUTosmc_axi_top):
    g = CovGroup("axi2ui write function")

    # cover point for fifo full, not necessary
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_aw_fifol1_io_fifo_wio_full,
                      {"aw_fifol1 is full": fc.Eq(1)}, name="aw_fifol1 full")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_aw_fifol2_io_fifo_wio_full,
                      {"aw_fifol2 is full": fc.Eq(1)}, name="aw_fifol2 full, ui_write_cmd full!")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_w_fifol1_io_fifo_wio_full,
                      {"w_fifol1 is full": fc.Eq(1)}, name="w_fifol1 full")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_w_fifol2_io_fifo_wio_full,
                      {"w_fifol2 is full": fc.Eq(1)}, name="w_fifol2 full, ui_write_data full!")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_wb_fifo_io_fifo_wio_full,
                      {"wb_fifo is full": fc.Eq(1)}, name="wb_fifo full")
    g.add_cover_point(axi2ui.osmc_axi_top_u_axi_write__u_axi_awb_fifo_out_io_fifo_wio_full,
                      {"awb_fifo_out is full": fc.Eq(1)}, name="awb_fifo_out full")
    
    # axi aw output signal: awready
    g.add_cover_point((toffee.Delayer(axi2ui.io_awio_awready, 1), (toffee.Delayer(axi2ui.io_awio_awvalid, 1)),
                       axi2ui.io_awio_awready, axi2ui.io_awio_awvalid), {
        "axi awready is set 1 before awvalid":
            lambda signal: signal[0].value == 1 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_awready_before_awvalid")
    g.add_cover_point((toffee.Delayer(axi2ui.io_awio_awready, 1), (toffee.Delayer(axi2ui.io_awio_awvalid, 1)),
                       axi2ui.io_awio_awready, axi2ui.io_awio_awvalid), {
        "axi awready is set 1 after awvalid":
            lambda signal: signal[0].value == 0 and signal[1].value == 1 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_awready_after_awvalid")
    g.add_cover_point((toffee.Delayer(axi2ui.io_awio_awready, 1), (toffee.Delayer(axi2ui.io_awio_awvalid, 1)),
                       axi2ui.io_awio_awready, axi2ui.io_awio_awvalid), {
        "axi awready and awvalid is set 1 at the same cycle":
            lambda signal: signal[0].value == 0 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_awready_with_awvalid")
    
    # axi w output signal: wready
    g.add_cover_point((toffee.Delayer(axi2ui.io_wio_wready, 1), (toffee.Delayer(axi2ui.io_wio_wvalid, 1)),
                       axi2ui.io_wio_wready, axi2ui.io_wio_wvalid), {
        "axi wready is set 1 before wvalid":
            lambda signal: signal[0].value == 1 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_wready_before_wvalid")
    g.add_cover_point((toffee.Delayer(axi2ui.io_wio_wready, 1), (toffee.Delayer(axi2ui.io_wio_wvalid, 1)),
                       axi2ui.io_wio_wready, axi2ui.io_wio_wvalid), {
        "axi wready is set 1 after wvalid":
            lambda signal: signal[0].value == 0 and signal[1].value == 1 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_wready_after_wvalid")
    g.add_cover_point((toffee.Delayer(axi2ui.io_wio_wready, 1), (toffee.Delayer(axi2ui.io_wio_wvalid, 1)),
                       axi2ui.io_wio_wready, axi2ui.io_wio_wvalid), {
        "axi wready and wvalid is set 1 at the same cycle":
            lambda signal: signal[0].value == 0 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_wready_with_wvalid")
    
    # axi b output signal: bvalid
    g.add_cover_point((toffee.Delayer(axi2ui.io_bio_bvalid, 1), (toffee.Delayer(axi2ui.io_bio_bready, 1)),
                       axi2ui.io_bio_bvalid, axi2ui.io_bio_bready), {
        "axi bvalid is set 1 before bready":
            lambda signal: signal[0].value == 1 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_bvalid_before_bready")
    g.add_cover_point((toffee.Delayer(axi2ui.io_bio_bvalid, 1), (toffee.Delayer(axi2ui.io_bio_bready, 1)),
                       axi2ui.io_bio_bvalid, axi2ui.io_bio_bready), {
        "axi bvalid and bready is set 1 at the same cycle":
            lambda signal: signal[0].value == 0 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="axi_bvalid_with_bready")
    
    # ui aw output signal: awvalid
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_awio_valid, 1), (toffee.Delayer(axi2ui.io_ui_awio_ready, 1)),
                       axi2ui.io_ui_awio_valid, axi2ui.io_ui_awio_ready), {
        "ui awvalid is set 1 before awready":
            lambda signal: signal[0].value == 1 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_awvalid_before_awready")
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_awio_valid, 1), (toffee.Delayer(axi2ui.io_ui_awio_ready, 1)),
                       axi2ui.io_ui_awio_valid, axi2ui.io_ui_awio_ready), {
        "ui awvalid is set 1 after awready":
            lambda signal: signal[0].value == 0 and signal[1].value == 1 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_awvalid_after_awready")
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_awio_valid, 1), (toffee.Delayer(axi2ui.io_ui_awio_ready, 1)),
                       axi2ui.io_ui_awio_valid, axi2ui.io_ui_awio_ready), {
        "ui awvalid and awready is set 1 at the same cycle":
            lambda signal: signal[0].value == 0 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_awvalid_with_awready")
    
    # ui w output signal: wvalid
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_wio_valid, 1), (toffee.Delayer(axi2ui.io_ui_wio_ready, 1)),
                       axi2ui.io_ui_wio_valid, axi2ui.io_ui_wio_ready), {
        "ui wvalid is set 1 before wready":
            lambda signal: signal[0].value == 1 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_wvalid_before_wready")
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_wio_valid, 1), (toffee.Delayer(axi2ui.io_ui_wio_ready, 1)),
                       axi2ui.io_ui_wio_valid, axi2ui.io_ui_wio_ready), {
        "ui wvalid is set 1 after wready":
            lambda signal: signal[0].value == 0 and signal[1].value == 1 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_wvalid_after_wready")
    g.add_cover_point((toffee.Delayer(axi2ui.io_ui_wio_valid, 1), (toffee.Delayer(axi2ui.io_ui_wio_ready, 1)),
                       axi2ui.io_ui_wio_valid, axi2ui.io_ui_wio_ready), {
        "ui wvalid and wready is set 1 at the same cycle":
            lambda signal: signal[0].value == 0 and signal[1].value == 0 and signal[2].value == 1 and signal[3].value == 1
    }, name="ui_wvalid_with_wready")
    
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

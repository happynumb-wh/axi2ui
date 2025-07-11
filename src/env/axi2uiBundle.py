from utils.mcparam import *
from toffee import Bundle, Signals, Signal


# Write address channel
class axiAwioBundle(Bundle):
    awid, \
    awaddr, \
    awlen, \
    awsize, \
    awburst, \
    awuser, \
    awqos, \
    awvalid, \
    awready = Signals(9)

# Write data channel
class axiWioBundle(Bundle):
    wuser, \
    wdata, \
    wstrb, \
    wlast, \
    wvalid, \
    wready = Signals(6)

# Wrirtes response channel
class axiBioBundle(Bundle):
    bid, \
    bresp, \
    buser, \
    bvalid, \
    bready = Signals(5)

# Read address channel
class axiArioBundle(Bundle):
    arid, \
    araddr, \
    arlen, \
    arsize, \
    arburst, \
    aruser, \
    arqos, \
    arvalid, \
    arready = Signals(9)

# Read data channel
class axiRioBundle(Bundle):
    rid, \
    ruser, \
    rdata, \
    rresp, \
    rlast, \
    rvalid, \
    rready = Signals(7)

# UI write address channel
class axiUiAwioBundle(Bundle):
    ready, \
    valid, \
    bits_addr, \
    bits_token, \
    bits_pri = Signals(5)

# UI write data channel
class axiUiWioBundle(Bundle):
    ready, \
    valid, \
    bits_wdata, \
    bits_wstrb = Signals(4)

# UI read address channel
class axiUiArioBundle(Bundle):
    ready, \
    valid, \
    bits_addr, \
    bits_token, \
    bits_pri = Signals(5)

# UI read data channel
class axiUiRioBundle(Bundle):
    ready, \
    valid, \
    bits_rdata, \
    bits_rtoken = Signals(4)

# AXI read bundle
class axiReadBundle(Bundle):
    ario = axiArioBundle().from_prefix("io_ario_")
    rio = axiRioBundle().from_prefix("io_rio_")

# AXI write bundle
class axiWriteBundle(Bundle):
    awio = axiAwioBundle().from_prefix("io_awio_")
    wio = axiWioBundle().from_prefix("io_wio_")
    bio = axiBioBundle().from_prefix("io_bio_")

# AXI master bundle
class axiMasterBundle(Bundle):
    clock, reset = Signals(2)
    writeBundle = axiWriteBundle()
    readBundle = axiReadBundle()


# ui read bundle
class uiReadBundle(Bundle):
    ario = axiUiArioBundle().from_prefix("io_ui_ario_")
    rio = axiUiRioBundle().from_prefix("io_ui_rio_")

# ui write bundle
class uiWriteBundle(Bundle):
    awio = axiUiAwioBundle().from_prefix("io_ui_awio_")
    wio = axiUiWioBundle().from_prefix("io_ui_wio_")

# uiSlaveBundle
class uiSlaveBundle(Bundle):
    writeBundle = uiWriteBundle()
    readBundle = uiReadBundle()

class axiReadBurstClipBundle(Bundle):
    io_rrob_io_rvalid, \
    io_fifol1_rwio_wen, \
    io_cmd_fifo_rio_ren, \
    io_cmd_fifo_rio_rdata = Signals(4)

class cornorTestBundle(Bundle):
    axi_write_burst_clip = axiReadBurstClipBundle().from_prefix("osmc_axi_top_u_axi_read_u_axi_read_burst_clip_")
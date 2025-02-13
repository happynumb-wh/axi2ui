#coding=utf8

try:
    from . import xspcomm as xsp
except Exception as e:
    import xspcomm as xsp

if __package__ or "." in __name__:
    from .libUT_osmc_axi_top import *
else:
    from libUT_osmc_axi_top import *


class DUTosmc_axi_top(object):

    # initialize
    def __init__(self, *args, **kwargs):
        self.dut = DutUnifiedBase(*args)
        self.xclock = xsp.XClock(self.dut.simStep)
        self.xport  = xsp.XPort()
        self.xclock.Add(self.xport)
        self.event = self.xclock.getEvent()
        self.internal_signals = {}
        # set output files
        if kwargs.get("waveform_filename"):
            self.dut.SetWaveform(kwargs.get("waveform_filename"))
        if kwargs.get("coverage_filename"):
            self.dut.SetCoverage(kwargs.get("coverage_filename"))

        # all Pins
        self.clock = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.reset = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_awio_awid = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_awio_awaddr = xsp.XPin(xsp.XData(36, xsp.XData.In), self.event)
        self.io_awio_awlen = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_awio_awsize = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.io_awio_awburst = xsp.XPin(xsp.XData(2, xsp.XData.In), self.event)
        self.io_awio_awuser = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_awio_awqos = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.io_awio_awvalid = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_awio_awready = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_wio_wid = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_wio_wuser = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wio_wdata = xsp.XPin(xsp.XData(256, xsp.XData.In), self.event)
        self.io_wio_wstrb = xsp.XPin(xsp.XData(32, xsp.XData.In), self.event)
        self.io_wio_wlast = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wio_wvalid = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_wio_wready = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_bio_bid = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)
        self.io_bio_bresp = xsp.XPin(xsp.XData(2, xsp.XData.Out), self.event)
        self.io_bio_buser = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_bio_bvalid = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_bio_bready = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ario_arid = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_ario_araddr = xsp.XPin(xsp.XData(36, xsp.XData.In), self.event)
        self.io_ario_arlen = xsp.XPin(xsp.XData(8, xsp.XData.In), self.event)
        self.io_ario_arsize = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.io_ario_arburst = xsp.XPin(xsp.XData(2, xsp.XData.In), self.event)
        self.io_ario_aruser = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ario_arqos = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.io_ario_arvalid = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ario_arready = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rio_rid = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)
        self.io_rio_ruser = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rio_rdata = xsp.XPin(xsp.XData(256, xsp.XData.Out), self.event)
        self.io_rio_rresp = xsp.XPin(xsp.XData(2, xsp.XData.Out), self.event)
        self.io_rio_rlast = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rio_rvalid = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_rio_rready = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ui_awio_ready = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ui_awio_valid = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_awio_bits_addr = xsp.XPin(xsp.XData(36, xsp.XData.Out), self.event)
        self.io_ui_awio_bits_token = xsp.XPin(xsp.XData(10, xsp.XData.Out), self.event)
        self.io_ui_awio_bits_pri = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_wio_ready = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ui_wio_valid = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_wio_bits_wdata = xsp.XPin(xsp.XData(512, xsp.XData.Out), self.event)
        self.io_ui_wio_bits_wstrb = xsp.XPin(xsp.XData(64, xsp.XData.Out), self.event)
        self.io_ui_ario_ready = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ui_ario_valid = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_ario_bits_addr = xsp.XPin(xsp.XData(36, xsp.XData.Out), self.event)
        self.io_ui_ario_bits_token = xsp.XPin(xsp.XData(10, xsp.XData.Out), self.event)
        self.io_ui_ario_bits_pri = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_rio_ready = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_ui_rio_valid = xsp.XPin(xsp.XData(0, xsp.XData.In), self.event)
        self.io_ui_rio_bits_rdata = xsp.XPin(xsp.XData(512, xsp.XData.In), self.event)
        self.io_ui_rio_bits_rtoken = xsp.XPin(xsp.XData(10, xsp.XData.In), self.event)
        self.io_a2uregio_axiRdCmdCnt = xsp.XPin(xsp.XData(32, xsp.XData.Out), self.event)
        self.io_a2uregio_axiWrCmdCnt = xsp.XPin(xsp.XData(32, xsp.XData.Out), self.event)
        self.io_a2uregio_uiRdCmdCnt = xsp.XPin(xsp.XData(32, xsp.XData.Out), self.event)
        self.io_a2uregio_uiWrCmdCnt = xsp.XPin(xsp.XData(32, xsp.XData.Out), self.event)
        self.io_a2uregio_uiRbCmdCnt = xsp.XPin(xsp.XData(32, xsp.XData.Out), self.event)
        self.io_a2uregio_readyStall = xsp.XPin(xsp.XData(0, xsp.XData.Out), self.event)
        self.io_a2uregio_tokenCnt = xsp.XPin(xsp.XData(8, xsp.XData.Out), self.event)


        # BindDPI
        self.clock.BindDPIPtr(self.dut.GetDPIHandle("clock", 0), self.dut.GetDPIHandle("clock", 1))
        self.reset.BindDPIPtr(self.dut.GetDPIHandle("reset", 0), self.dut.GetDPIHandle("reset", 1))
        self.io_awio_awid.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awid", 0), self.dut.GetDPIHandle("io_awio_awid", 1))
        self.io_awio_awaddr.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awaddr", 0), self.dut.GetDPIHandle("io_awio_awaddr", 1))
        self.io_awio_awlen.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awlen", 0), self.dut.GetDPIHandle("io_awio_awlen", 1))
        self.io_awio_awsize.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awsize", 0), self.dut.GetDPIHandle("io_awio_awsize", 1))
        self.io_awio_awburst.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awburst", 0), self.dut.GetDPIHandle("io_awio_awburst", 1))
        self.io_awio_awuser.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awuser", 0), self.dut.GetDPIHandle("io_awio_awuser", 1))
        self.io_awio_awqos.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awqos", 0), self.dut.GetDPIHandle("io_awio_awqos", 1))
        self.io_awio_awvalid.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awvalid", 0), self.dut.GetDPIHandle("io_awio_awvalid", 1))
        self.io_awio_awready.BindDPIPtr(self.dut.GetDPIHandle("io_awio_awready", 0), self.dut.GetDPIHandle("io_awio_awready", 1))
        self.io_wio_wid.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wid", 0), self.dut.GetDPIHandle("io_wio_wid", 1))
        self.io_wio_wuser.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wuser", 0), self.dut.GetDPIHandle("io_wio_wuser", 1))
        self.io_wio_wdata.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wdata", 0), self.dut.GetDPIHandle("io_wio_wdata", 1))
        self.io_wio_wstrb.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wstrb", 0), self.dut.GetDPIHandle("io_wio_wstrb", 1))
        self.io_wio_wlast.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wlast", 0), self.dut.GetDPIHandle("io_wio_wlast", 1))
        self.io_wio_wvalid.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wvalid", 0), self.dut.GetDPIHandle("io_wio_wvalid", 1))
        self.io_wio_wready.BindDPIPtr(self.dut.GetDPIHandle("io_wio_wready", 0), self.dut.GetDPIHandle("io_wio_wready", 1))
        self.io_bio_bid.BindDPIPtr(self.dut.GetDPIHandle("io_bio_bid", 0), self.dut.GetDPIHandle("io_bio_bid", 1))
        self.io_bio_bresp.BindDPIPtr(self.dut.GetDPIHandle("io_bio_bresp", 0), self.dut.GetDPIHandle("io_bio_bresp", 1))
        self.io_bio_buser.BindDPIPtr(self.dut.GetDPIHandle("io_bio_buser", 0), self.dut.GetDPIHandle("io_bio_buser", 1))
        self.io_bio_bvalid.BindDPIPtr(self.dut.GetDPIHandle("io_bio_bvalid", 0), self.dut.GetDPIHandle("io_bio_bvalid", 1))
        self.io_bio_bready.BindDPIPtr(self.dut.GetDPIHandle("io_bio_bready", 0), self.dut.GetDPIHandle("io_bio_bready", 1))
        self.io_ario_arid.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arid", 0), self.dut.GetDPIHandle("io_ario_arid", 1))
        self.io_ario_araddr.BindDPIPtr(self.dut.GetDPIHandle("io_ario_araddr", 0), self.dut.GetDPIHandle("io_ario_araddr", 1))
        self.io_ario_arlen.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arlen", 0), self.dut.GetDPIHandle("io_ario_arlen", 1))
        self.io_ario_arsize.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arsize", 0), self.dut.GetDPIHandle("io_ario_arsize", 1))
        self.io_ario_arburst.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arburst", 0), self.dut.GetDPIHandle("io_ario_arburst", 1))
        self.io_ario_aruser.BindDPIPtr(self.dut.GetDPIHandle("io_ario_aruser", 0), self.dut.GetDPIHandle("io_ario_aruser", 1))
        self.io_ario_arqos.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arqos", 0), self.dut.GetDPIHandle("io_ario_arqos", 1))
        self.io_ario_arvalid.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arvalid", 0), self.dut.GetDPIHandle("io_ario_arvalid", 1))
        self.io_ario_arready.BindDPIPtr(self.dut.GetDPIHandle("io_ario_arready", 0), self.dut.GetDPIHandle("io_ario_arready", 1))
        self.io_rio_rid.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rid", 0), self.dut.GetDPIHandle("io_rio_rid", 1))
        self.io_rio_ruser.BindDPIPtr(self.dut.GetDPIHandle("io_rio_ruser", 0), self.dut.GetDPIHandle("io_rio_ruser", 1))
        self.io_rio_rdata.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rdata", 0), self.dut.GetDPIHandle("io_rio_rdata", 1))
        self.io_rio_rresp.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rresp", 0), self.dut.GetDPIHandle("io_rio_rresp", 1))
        self.io_rio_rlast.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rlast", 0), self.dut.GetDPIHandle("io_rio_rlast", 1))
        self.io_rio_rvalid.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rvalid", 0), self.dut.GetDPIHandle("io_rio_rvalid", 1))
        self.io_rio_rready.BindDPIPtr(self.dut.GetDPIHandle("io_rio_rready", 0), self.dut.GetDPIHandle("io_rio_rready", 1))
        self.io_ui_awio_ready.BindDPIPtr(self.dut.GetDPIHandle("io_ui_awio_ready", 0), self.dut.GetDPIHandle("io_ui_awio_ready", 1))
        self.io_ui_awio_valid.BindDPIPtr(self.dut.GetDPIHandle("io_ui_awio_valid", 0), self.dut.GetDPIHandle("io_ui_awio_valid", 1))
        self.io_ui_awio_bits_addr.BindDPIPtr(self.dut.GetDPIHandle("io_ui_awio_bits_addr", 0), self.dut.GetDPIHandle("io_ui_awio_bits_addr", 1))
        self.io_ui_awio_bits_token.BindDPIPtr(self.dut.GetDPIHandle("io_ui_awio_bits_token", 0), self.dut.GetDPIHandle("io_ui_awio_bits_token", 1))
        self.io_ui_awio_bits_pri.BindDPIPtr(self.dut.GetDPIHandle("io_ui_awio_bits_pri", 0), self.dut.GetDPIHandle("io_ui_awio_bits_pri", 1))
        self.io_ui_wio_ready.BindDPIPtr(self.dut.GetDPIHandle("io_ui_wio_ready", 0), self.dut.GetDPIHandle("io_ui_wio_ready", 1))
        self.io_ui_wio_valid.BindDPIPtr(self.dut.GetDPIHandle("io_ui_wio_valid", 0), self.dut.GetDPIHandle("io_ui_wio_valid", 1))
        self.io_ui_wio_bits_wdata.BindDPIPtr(self.dut.GetDPIHandle("io_ui_wio_bits_wdata", 0), self.dut.GetDPIHandle("io_ui_wio_bits_wdata", 1))
        self.io_ui_wio_bits_wstrb.BindDPIPtr(self.dut.GetDPIHandle("io_ui_wio_bits_wstrb", 0), self.dut.GetDPIHandle("io_ui_wio_bits_wstrb", 1))
        self.io_ui_ario_ready.BindDPIPtr(self.dut.GetDPIHandle("io_ui_ario_ready", 0), self.dut.GetDPIHandle("io_ui_ario_ready", 1))
        self.io_ui_ario_valid.BindDPIPtr(self.dut.GetDPIHandle("io_ui_ario_valid", 0), self.dut.GetDPIHandle("io_ui_ario_valid", 1))
        self.io_ui_ario_bits_addr.BindDPIPtr(self.dut.GetDPIHandle("io_ui_ario_bits_addr", 0), self.dut.GetDPIHandle("io_ui_ario_bits_addr", 1))
        self.io_ui_ario_bits_token.BindDPIPtr(self.dut.GetDPIHandle("io_ui_ario_bits_token", 0), self.dut.GetDPIHandle("io_ui_ario_bits_token", 1))
        self.io_ui_ario_bits_pri.BindDPIPtr(self.dut.GetDPIHandle("io_ui_ario_bits_pri", 0), self.dut.GetDPIHandle("io_ui_ario_bits_pri", 1))
        self.io_ui_rio_ready.BindDPIPtr(self.dut.GetDPIHandle("io_ui_rio_ready", 0), self.dut.GetDPIHandle("io_ui_rio_ready", 1))
        self.io_ui_rio_valid.BindDPIPtr(self.dut.GetDPIHandle("io_ui_rio_valid", 0), self.dut.GetDPIHandle("io_ui_rio_valid", 1))
        self.io_ui_rio_bits_rdata.BindDPIPtr(self.dut.GetDPIHandle("io_ui_rio_bits_rdata", 0), self.dut.GetDPIHandle("io_ui_rio_bits_rdata", 1))
        self.io_ui_rio_bits_rtoken.BindDPIPtr(self.dut.GetDPIHandle("io_ui_rio_bits_rtoken", 0), self.dut.GetDPIHandle("io_ui_rio_bits_rtoken", 1))
        self.io_a2uregio_axiRdCmdCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_axiRdCmdCnt", 0), self.dut.GetDPIHandle("io_a2uregio_axiRdCmdCnt", 1))
        self.io_a2uregio_axiWrCmdCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_axiWrCmdCnt", 0), self.dut.GetDPIHandle("io_a2uregio_axiWrCmdCnt", 1))
        self.io_a2uregio_uiRdCmdCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_uiRdCmdCnt", 0), self.dut.GetDPIHandle("io_a2uregio_uiRdCmdCnt", 1))
        self.io_a2uregio_uiWrCmdCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_uiWrCmdCnt", 0), self.dut.GetDPIHandle("io_a2uregio_uiWrCmdCnt", 1))
        self.io_a2uregio_uiRbCmdCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_uiRbCmdCnt", 0), self.dut.GetDPIHandle("io_a2uregio_uiRbCmdCnt", 1))
        self.io_a2uregio_readyStall.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_readyStall", 0), self.dut.GetDPIHandle("io_a2uregio_readyStall", 1))
        self.io_a2uregio_tokenCnt.BindDPIPtr(self.dut.GetDPIHandle("io_a2uregio_tokenCnt", 0), self.dut.GetDPIHandle("io_a2uregio_tokenCnt", 1))


        # Add2Port
        self.xport.Add("clock", self.clock.xdata)
        self.xport.Add("reset", self.reset.xdata)
        self.xport.Add("io_awio_awid", self.io_awio_awid.xdata)
        self.xport.Add("io_awio_awaddr", self.io_awio_awaddr.xdata)
        self.xport.Add("io_awio_awlen", self.io_awio_awlen.xdata)
        self.xport.Add("io_awio_awsize", self.io_awio_awsize.xdata)
        self.xport.Add("io_awio_awburst", self.io_awio_awburst.xdata)
        self.xport.Add("io_awio_awuser", self.io_awio_awuser.xdata)
        self.xport.Add("io_awio_awqos", self.io_awio_awqos.xdata)
        self.xport.Add("io_awio_awvalid", self.io_awio_awvalid.xdata)
        self.xport.Add("io_awio_awready", self.io_awio_awready.xdata)
        self.xport.Add("io_wio_wid", self.io_wio_wid.xdata)
        self.xport.Add("io_wio_wuser", self.io_wio_wuser.xdata)
        self.xport.Add("io_wio_wdata", self.io_wio_wdata.xdata)
        self.xport.Add("io_wio_wstrb", self.io_wio_wstrb.xdata)
        self.xport.Add("io_wio_wlast", self.io_wio_wlast.xdata)
        self.xport.Add("io_wio_wvalid", self.io_wio_wvalid.xdata)
        self.xport.Add("io_wio_wready", self.io_wio_wready.xdata)
        self.xport.Add("io_bio_bid", self.io_bio_bid.xdata)
        self.xport.Add("io_bio_bresp", self.io_bio_bresp.xdata)
        self.xport.Add("io_bio_buser", self.io_bio_buser.xdata)
        self.xport.Add("io_bio_bvalid", self.io_bio_bvalid.xdata)
        self.xport.Add("io_bio_bready", self.io_bio_bready.xdata)
        self.xport.Add("io_ario_arid", self.io_ario_arid.xdata)
        self.xport.Add("io_ario_araddr", self.io_ario_araddr.xdata)
        self.xport.Add("io_ario_arlen", self.io_ario_arlen.xdata)
        self.xport.Add("io_ario_arsize", self.io_ario_arsize.xdata)
        self.xport.Add("io_ario_arburst", self.io_ario_arburst.xdata)
        self.xport.Add("io_ario_aruser", self.io_ario_aruser.xdata)
        self.xport.Add("io_ario_arqos", self.io_ario_arqos.xdata)
        self.xport.Add("io_ario_arvalid", self.io_ario_arvalid.xdata)
        self.xport.Add("io_ario_arready", self.io_ario_arready.xdata)
        self.xport.Add("io_rio_rid", self.io_rio_rid.xdata)
        self.xport.Add("io_rio_ruser", self.io_rio_ruser.xdata)
        self.xport.Add("io_rio_rdata", self.io_rio_rdata.xdata)
        self.xport.Add("io_rio_rresp", self.io_rio_rresp.xdata)
        self.xport.Add("io_rio_rlast", self.io_rio_rlast.xdata)
        self.xport.Add("io_rio_rvalid", self.io_rio_rvalid.xdata)
        self.xport.Add("io_rio_rready", self.io_rio_rready.xdata)
        self.xport.Add("io_ui_awio_ready", self.io_ui_awio_ready.xdata)
        self.xport.Add("io_ui_awio_valid", self.io_ui_awio_valid.xdata)
        self.xport.Add("io_ui_awio_bits_addr", self.io_ui_awio_bits_addr.xdata)
        self.xport.Add("io_ui_awio_bits_token", self.io_ui_awio_bits_token.xdata)
        self.xport.Add("io_ui_awio_bits_pri", self.io_ui_awio_bits_pri.xdata)
        self.xport.Add("io_ui_wio_ready", self.io_ui_wio_ready.xdata)
        self.xport.Add("io_ui_wio_valid", self.io_ui_wio_valid.xdata)
        self.xport.Add("io_ui_wio_bits_wdata", self.io_ui_wio_bits_wdata.xdata)
        self.xport.Add("io_ui_wio_bits_wstrb", self.io_ui_wio_bits_wstrb.xdata)
        self.xport.Add("io_ui_ario_ready", self.io_ui_ario_ready.xdata)
        self.xport.Add("io_ui_ario_valid", self.io_ui_ario_valid.xdata)
        self.xport.Add("io_ui_ario_bits_addr", self.io_ui_ario_bits_addr.xdata)
        self.xport.Add("io_ui_ario_bits_token", self.io_ui_ario_bits_token.xdata)
        self.xport.Add("io_ui_ario_bits_pri", self.io_ui_ario_bits_pri.xdata)
        self.xport.Add("io_ui_rio_ready", self.io_ui_rio_ready.xdata)
        self.xport.Add("io_ui_rio_valid", self.io_ui_rio_valid.xdata)
        self.xport.Add("io_ui_rio_bits_rdata", self.io_ui_rio_bits_rdata.xdata)
        self.xport.Add("io_ui_rio_bits_rtoken", self.io_ui_rio_bits_rtoken.xdata)
        self.xport.Add("io_a2uregio_axiRdCmdCnt", self.io_a2uregio_axiRdCmdCnt.xdata)
        self.xport.Add("io_a2uregio_axiWrCmdCnt", self.io_a2uregio_axiWrCmdCnt.xdata)
        self.xport.Add("io_a2uregio_uiRdCmdCnt", self.io_a2uregio_uiRdCmdCnt.xdata)
        self.xport.Add("io_a2uregio_uiWrCmdCnt", self.io_a2uregio_uiWrCmdCnt.xdata)
        self.xport.Add("io_a2uregio_uiRbCmdCnt", self.io_a2uregio_uiRbCmdCnt.xdata)
        self.xport.Add("io_a2uregio_readyStall", self.io_a2uregio_readyStall.xdata)
        self.xport.Add("io_a2uregio_tokenCnt", self.io_a2uregio_tokenCnt.xdata)


        # Cascaded ports
        self.io = self.xport.NewSubPort("io_")
        self.io_a2uregio = self.xport.NewSubPort("io_a2uregio_")
        self.io_ario = self.xport.NewSubPort("io_ario_")
        self.io_awio = self.xport.NewSubPort("io_awio_")
        self.io_bio = self.xport.NewSubPort("io_bio_")
        self.io_rio = self.xport.NewSubPort("io_rio_")
        self.io_ui = self.xport.NewSubPort("io_ui_")
        self.io_ui_ario = self.xport.NewSubPort("io_ui_ario_")
        self.io_ui_ario_bits = self.xport.NewSubPort("io_ui_ario_bits_")
        self.io_ui_awio = self.xport.NewSubPort("io_ui_awio_")
        self.io_ui_awio_bits = self.xport.NewSubPort("io_ui_awio_bits_")
        self.io_ui_rio = self.xport.NewSubPort("io_ui_rio_")
        self.io_ui_rio_bits = self.xport.NewSubPort("io_ui_rio_bits_")
        self.io_ui_wio = self.xport.NewSubPort("io_ui_wio_")
        self.io_ui_wio_bits = self.xport.NewSubPort("io_ui_wio_bits_")
        self.io_wio = self.xport.NewSubPort("io_wio_")


    def __del__(self):
        self.Finish()

    ################################
    #         User APIs            #
    ################################
    def InitClock(self, name: str):
        self.xclock.Add(self.xport[name])

    def Step(self, i:int = 1):
        self.xclock.Step(i)

    def StepRis(self, callback, args=(), kwargs={}):
        self.xclock.StepRis(callback, args, kwargs)

    def StepFal(self, callback, args=(), kwargs={}):
        self.xclock.StepFal(callback, args, kwargs)

    def SetWaveform(self, filename: str):
        self.dut.SetWaveform(filename)
    
    def FlushWaveform(self):
        self.dut.FlushWaveform()

    def SetCoverage(self, filename: str):
        self.dut.SetCoverage(filename)
    
    def CheckPoint(self, name: str) -> int:
        self.dut.CheckPoint(name)

    def Restore(self, name: str) -> int:
        self.dut.Restore(name)

    def GetInternalSignal(self, name: str):
        if name not in self.internal_signals:
            signal = xsp.XData.FromVPI(self.dut.GetVPIHandleObj(name),
                                       self.dut.GetVPIFuncPtr("vpi_get"),
                                       self.dut.GetVPIFuncPtr("vpi_get_value"),
                                       self.dut.GetVPIFuncPtr("vpi_put_value"), name)
            if signal is None:
                return None
            self.internal_signals[name] = xsp.XPin(signal, self.event)
        return self.internal_signals[name]

    def VPIInternalSignalList(self, prefix="", deep=99):
        return self.dut.VPIInternalSignalList(prefix, deep)

    def Finish(self):
        self.dut.Finish()

    def RefreshComb(self):
        self.dut.RefreshComb()

    ################################
    #      End of User APIs        #
    ################################

    def __getitem__(self, key):
        return xsp.XPin(self.port[key], self.event)

    # Async APIs wrapped from XClock
    async def AStep(self,i: int):
        return await self.xclock.AStep(i)

    async def Acondition(self,fc_cheker):
        return await self.xclock.ACondition(fc_cheker)

    def RunStep(self,i: int):
        return self.xclock.RunStep(i)

    def __setattr__(self, name, value):
        assert not isinstance(getattr(self, name, None),
                              (xsp.XPin, xsp.XData)), \
        f"XPin and XData of DUT are read-only, do you mean to set the value of the signal? please use `{name}.value = ` instead."
        return super().__setattr__(name, value)


if __name__=="__main__":
    dut=DUTosmc_axi_top()
    dut.Step(100)

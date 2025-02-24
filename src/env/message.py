from toffee import Bundle, Signals, Signal

class axi2uiReadMessage:
    '''
    This class is used to create a message object that will be used to send and receive messages between the DUT and the agent.
    '''
    def __init__(self, bundle: Bundle):
        self.bundle = bundle
        # Read address channel
        self.arid = 0
        self.araddr = 0
        self.arlen = 0
        self.arsize = 0
        self.arburst = 0
        self.aruser = 0
        self.arqos = 0
        self.arvalid = 0
        self.arready = 0
        # Read data channel
        self.rid = 0
        self.ruser = 0
        self.rdata = 0
        self.rresp = 0
        self.rlast = 0
        self.rvalid = 0
        self.rready = 0
    
    def sampling(self):
        # Read address channel
        self.arid = self.bundle.ario.arid.value
        self.araddr = self.bundle.ario.araddr.value
        self.arlen = self.bundle.ario.arlen.value
        self.arsize = self.bundle.ario.arsize.value
        self.arburst = self.bundle.ario.arburst.value
        self.aruser = self.bundle.ario.aruser.value
        self.arqos = self.bundle.ario.arqos.value
        self.arvalid = self.bundle.ario.arvalid.value
        self.arready = self.bundle.ario.arready.value
        # Read data channel
        self.rid = self.bundle.rio.rid.value
        self.ruser = self.bundle.rio.ruser.value
        self.rdata = self.bundle.rio.rdata.value
        self.rresp = self.bundle.rio.rresp.value
        self.rlast = self.bundle.rio.rlast.value
        self.rvalid = self.bundle.rio.rvalid.value
        self.rready = self.bundle.rio.rready.value
    
    def __bundle_assign__(self, bundle: Bundle):
        # Read address channel
        bundle.ario.arid.value = self.arid
        bundle.ario.araddr.value = self.araddr
        bundle.ario.arlen.value = self.arlen
        bundle.ario.arsize.value = self.arsize
        bundle.ario.arburst.value = self.arburst
        bundle.ario.aruser.value = self.aruser
        bundle.ario.arqos.value = self.arqos
        bundle.ario.arvalid.value = self.arvalid
        # Read data channel
        bundle.rio.rready.value = self.rid

class axi2uiWriteMessage:
    '''
    This class is used to create a message object that will be used to send and receive messages between the DUT and the agent.
    '''
    def __init__(self, bundle: Bundle):
        self.bundle = bundle
        # Write address channel
        self.awid = 0
        self.awaddr = 0
        self.awlen = 0
        self.awsize = 0
        self.awburst = 0
        self.awuser = 0
        self.awqos = 0
        self.awvalid = 0
        self.awready = 0
        # Write data channel
        self.wid = 0
        self.wuser = 0
        self.wdata = 0
        self.wstrb = 0
        self.wlast = 0
        self.wvalid = 0
        self.wready = 0
        # Wrirtes response channel
        self.bid = 0
        self.bresp = 0
        self.buser = 0
        self.bvalid = 0
        self.bready = 0
    
    def sampling(self):
        # Write address channel
        self.awid = self.bundle.awio.awid.value
        self.awaddr = self.bundle.awio.awaddr.value
        self.awlen = self.bundle.awio.awlen.value
        self.awsize = self.bundle.awio.awsize.value
        self.awburst = self.bundle.awio.awburst.value
        self.awuser = self.bundle.awio.awuser.value
        self.awqos = self.bundle.awio.awqos.value
        self.awvalid = self.bundle.awio.awvalid.value
        self.awready = self.bundle.awio.awready.value
        # Write data channel
        self.wid = self.bundle.wio.wid.value
        self.wuser = self.bundle.wio.wuser.value
        self.wdata = self.bundle.wio.wdata.value
        self.wstrb = self.bundle.wio.wstrb.value
        self.wlast = self.bundle.wio.wlast.value
        self.wvalid = self.bundle.wio.wvalid.value
        self.wready = self.bundle.wio.wready.value
        # Wrirtes response channel
        self.bid = self.bundle.bio.bid.value
        self.bresp = self.bundle.bio.bresp.value
        self.buser = self.bundle.bio.buser.value
        self.bvalid = self.bundle.bio.bvalid.value
        self.bready = self.bundle.bio.bready.value
    
    def __bundle_assign__(self, bundle: Bundle):
        # Write address channel
        bundle.awio.awid.value = self.awid
        bundle.awio.awaddr.value = self.awaddr
        bundle.awio.awlen.value = self.awlen
        bundle.awio.awsize.value = self.awsize
        bundle.awio.awburst.value = self.awburst
        bundle.awio.awuser.value = self.awuser
        bundle.awio.awqos.value = self.awqos
        bundle.awio.awvalid.value = self.awvalid
        # Write data channel
        bundle.wio.wid.value = self.wid
        bundle.wio.wuser.value = self.wuser
        bundle.wio.wdata.value = self.wdata
        bundle.wio.wstrb.value = self.wstrb
        bundle.wio.wlast.value = self.wlast
        bundle.wio.wvalid.value = self.wvalid
        # Wrirtes response channel
        bundle.bio.bready.value = self.bready


class axi2uiMessage:
    '''
    This class is used to create a message object that will be used to send and receive messages between the DUT and the agent.
    '''
    def __init__(self, bundle: Bundle):
        self.bundle = bundle
        # Write address channel
        self.awid = 0
        self.awaddr = 0
        self.awlen = 0
        self.awsize = 0
        self.awburst = 0
        self.awuser = 0
        self.awqos = 0
        self.awvalid = 0
        self.awready = 0
        # Write data channel
        self.wid = 0
        self.wuser = 0
        self.wdata = 0
        self.wstrb = 0
        self.wlast = 0
        self.wvalid = 0
        self.wready = 0
        # Wrirtes response channel
        self.bid = 0
        self.bresp = 0
        self.buser = 0
        self.bvalid = 0
        self.bready = 0
        # Read address channel
        self.arid = 0
        self.araddr = 0
        self.arlen = 0
        self.arsize = 0
        self.arburst = 0
        self.aruser = 0
        self.arqos = 0
        self.arvalid = 0
        self.arready = 0
        # Read data channel
        self.rid = 0
        self.ruser = 0
        self.rdata = 0
        self.rresp = 0
        self.rlast = 0
        self.rvalid = 0
        self.rready = 0
    
    def sampling(self):
        # Write address channel
        self.awid = self.bundle.writeBundle.awio.awid.value
        self.awaddr = self.bundle.writeBundle.awio.awaddr.value
        self.awlen = self.bundle.writeBundle.awio.awlen.value
        self.awsize = self.bundle.writeBundle.awio.awsize.value
        self.awburst = self.bundle.writeBundle.awio.awburst.value
        self.awuser = self.bundle.writeBundle.awio.awuser.value
        self.awqos = self.bundle.writeBundle.awio.awqos.value
        self.awvalid = self.bundle.writeBundle.awio.awvalid.value
        self.awready = self.bundle.writeBundle.awio.awready.value
        # Write data channel
        self.wid = self.bundle.writeBundle.wio.wid.value
        self.wuser = self.bundle.writeBundle.wio.wuser.value
        self.wdata = self.bundle.writeBundle.wio.wdata.value
        self.wstrb = self.bundle.writeBundle.wio.wstrb.value
        self.wlast = self.bundle.writeBundle.wio.wlast.value
        self.wvalid = self.bundle.writeBundle.wio.wvalid.value
        self.wready = self.bundle.writeBundle.wio.wready.value
        # Wrirtes response channel
        self.bid = self.bundle.writeBundle.bio.bid.value
        self.bresp = self.bundle.writeBundle.bio.bresp.value
        self.buser = self.bundle.writeBundle.bio.buser.value
        self.bvalid = self.bundle.writeBundle.bio.bvalid.value
        self.bready = self.bundle.writeBundle.bio.bready.value
        # Read address channel
        self.arid = self.bundle.readBundle.ario.arid.value
        self.araddr = self.bundle.readBundle.ario.araddr.value
        self.arlen = self.bundle.readBundle.ario.arlen.value
        self.arsize = self.bundle.readBundle.ario.arsize.value
        self.arburst = self.bundle.readBundle.ario.arburst.value
        self.aruser = self.bundle.readBundle.ario.aruser.value
        self.arqos = self.bundle.readBundle.ario.arqos.value
        self.arvalid = self.bundle.readBundle.ario.arvalid.value
        self.arready = self.bundle.readBundle.ario.arready.value
        # Read data channel
        self.rid = self.bundle.readBundle.rio.rid.value
        self.ruser = self.bundle.readBundle.rio.ruser.value
        self.rdata = self.bundle.readBundle.rio.rdata.value
        self.rresp = self.bundle.readBundle.rio.rresp.value
        self.rlast = self.bundle.readBundle.rio.rlast.value
        self.rvalid = self.bundle.readBundle.rio.rvalid.value
        self.rready = self.bundle.readBundle.rio.rready.value
    
    def __bundle_assign__(self, bundle: Bundle):
        # Write address channel
        bundle.writeBundle.awio.awid.value = self.awid
        bundle.writeBundle.awio.awaddr.value = self.awaddr
        bundle.writeBundle.awio.awlen.value = self.awlen
        bundle.writeBundle.awio.awsize.value = self.awsize
        bundle.writeBundle.awio.awburst.value = self.awburst
        bundle.writeBundle.awio.awuser.value = self.awuser
        bundle.writeBundle.awio.awqos.value = self.awqos
        bundle.writeBundle.awio.awvalid.value = self.awvalid
        # Write data channel
        bundle.writeBundle.wio.wid.value = self.wid
        bundle.writeBundle.wio.wuser.value = self.wuser
        bundle.writeBundle.wio.wdata.value = self.wdata
        bundle.writeBundle.wio.wstrb.value = self.wstrb
        bundle.writeBundle.wio.wlast.value = self.wlast
        bundle.writeBundle.wio.wvalid.value = self.wvalid
        # Wrirtes response channel
        bundle.bio.bready.value = self.bready
        # Read address channel
        bundle.readBundle.ario.arid.value = self.arid
        bundle.readBundle.ario.araddr.value = self.araddr
        bundle.readBundle.ario.arlen.value = self.arlen
        bundle.readBundle.ario.arsize.value = self.arsize
        bundle.readBundle.ario.arburst.value = self.arburst
        bundle.readBundle.ario.aruser.value = self.aruser
        bundle.readBundle.ario.arqos.value = self.arqos
        bundle.readBundle.ario.arvalid.value = self.arvalid
        # Read data channel
        bundle.readBundle.rio.rready.value = self.rid
        
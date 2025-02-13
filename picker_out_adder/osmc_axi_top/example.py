try:
    from UT_osmc_axi_top import *
except:
    try:
        from osmc_axi_top import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTosmc_axi_top()
    # dut.init_clock("clk")

    dut.Step(1)

    dut.Finish()

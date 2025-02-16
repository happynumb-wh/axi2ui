#!/bin/python3
from axi2ui import *
from axi_virtual_master import *
from ui_virtual_slave import *
from scorebord import *
import sys


class OsmcAxiTopDriver:
    def __init__(self, dut, model:axi_virtual_master, port_dict:dict):
        self.dut = dut
        self.model = model
        self.port_dict = port_dict
        pass



def axi2ui_test(dut:DUTosmc_axi_top, tfile:str):
    scorebord = scoreBord(dut)
    axiVirtualMaster = axi_virtual_master(dut, scorebord)
    uiVirtualSlave = ui_virtual_slave(dut, scorebord)
    # init clock
    dut.InitClock("clock")
    # reset
    dut.reset.value = 1
    axiVirtualMaster.reset()
    dut.Step(20)
    dut.reset.value = 0
    dut.Step(20)

    # Write machine and Read machine
    dut.StepRis(axiVirtualMaster.axiReadMachine)
    dut.StepRis(axiVirtualMaster.axiWriteMachine)
    
    # ui slave respond
    dut.StepRis(uiVirtualSlave.awrioHandShake)
    dut.StepRis(uiVirtualSlave.wrioHandShake)
    
    # i = 0
    test_time = 0
    with open(tfile, "r") as f:
        for line in f:
            if "R" in line:
                id, time, type, addr = line.split(" ")
                test_time += 1
                
                while axiVirtualMaster.rstatus != axiVirtualMaster.Status.IDLE:
                    dut.Step(1)
                axiVirtualMaster.axi_ario(int(addr, 16), 0x2, 0x5, axiVirtualMaster.burst_length - 1)
                dut.Step(1)
            elif "W" in line:
                id, time, type, addr = line.split(" ")
                test_time += 1
                while axiVirtualMaster.wstatus != axiVirtualMaster.Status.IDLE:
                    dut.Step(1)
                axiVirtualMaster.axi_awio(int(addr, 16), 0x2, 0x5, axiVirtualMaster.burst_length - 1)
                dut.Step(1)
            else:
                print("Error: Unknow command")
                dut.Finish()
                exit(0)
        
    # f.close()
    addr = 0x10000000
    times = 100000
    # uiVirtualSlave.setWriteDelay(100000)
    # axiVirtualMaster.axi_ario(addr, 0x2, 0x5, axiVirtualMaster.burst_length - 1)
    # dut.Step(100)
    
    for i in range(times):
        while axiVirtualMaster.wstatus != axiVirtualMaster.Status.IDLE:
            dut.Step(1)
        axiVirtualMaster.axi_awio(addr + i * 0x100, 0x2, 0x5, axiVirtualMaster.burst_length - 1)
        dut.Step(1)

    dut.Finish()
    
    # dut.Step(100)
    print("axi2ui_test")
    pass





if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f'Trace file {sys.argv[1]}')
    else:
        print("No trace file")
        exit(1)
    print("Begin test axi2ui")
    dut = DUTosmc_axi_top()
    axi2ui_test(dut, sys.argv[1])
    dut.Finish()
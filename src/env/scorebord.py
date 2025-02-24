from utils import mcparam
import random

class scoreBord:
    def __init__(self):
        self.virtualMemory = {}
    
    
    def writeMemory(self, addr, data):
        self.virtualMemory[addr] = data
    # Read memory
    def readMemory(self, addr):
        if self.virtualMemory.get(addr) == None:
            self.virtualMemory[addr] = random.randint(0, 2**mcparam.UI_DATAW - 1)
        return self.virtualMemory[addr]


    
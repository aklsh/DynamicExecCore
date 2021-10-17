from collections import namedtuple
from memory import mem

fuEntry = namedtuple('fuEntry', 'instrId, regVal, opCode')

class ASU:
    '''
        Add/Sub Functional Unit
        Execution is pipelined with 1 instr fed in each cycle
        latency of FU is as mentioned in config.py
    '''
    def __init__(self, latency):
        self.latency = latency
        '''
            InstrIdx => Reorder Buffer index, RegVal => value to be written to RenameReg & forwarded
            opCode: 1 => add, 0 => sub
        '''
        self.stages = []
        for _ in range(self.latency):
            temp = fuEntry(-1, None, -1)
            self.stages.extend([temp])

    def shiftAndEval(self, index= -1, opCode= -1, op1=None, op2=None):
        '''
            Note: If the RS is full, issue a NOP (so that the output value is got)
                  by passing the default values to shiftAndEval()
        '''
        out = self.stages[-1]
        self.stages[1:] = self.stages[0:-1]     # shift (pipelined exec)
        if (opCode == -1):                      # NOP bubble
            regval = None
        else:
            if opCode == 'ADD':
                regval = op1 + op2
            elif opCode == 'SUB':
                regval = op1 - op2
            else:
                index = -1
                regval = None
        self.stages[0] = fuEntry(index, regval, opCode)
        return out

class MU:
    '''
        Mult Functional Unit
        Execution is pipelined with 1 instr fed in each cycle
        latency of FU is as mentioned in config.py
    '''
    def __init__(self, latency):
        self.latency = latency
        '''
            InstrIdx => Reorder Buffer index, RegVal => value to be written to RenameReg & forwarded
            opCode: 1 => add, 0 => sub
        '''
        self.stages = []
        for _ in range(self.latency):
            temp = fuEntry(-1, None, -1)
            self.stages.extend([temp])

    def shiftAndEval(self, index= -1, opCode= -1, op1=None, op2=None):
        '''
            Note: If the RS is full, issue a NOP (so that the output value is got)
                  by passing the default values to shiftAndEval()
        '''
        out = self.stages[-1]
        self.stages[1:] = self.stages[0:-1]     # shift (pipelined exec)
        if (opCode == -1):      # NOP bubble
            regval = None
        else:
            if opCode == 'MUL':
                regval = op1*op2
            else:
                index = -1
                regval = None
        self.stages[0] = fuEntry(index, regval, opCode)
        return out

class DU:
    '''
        Div Functional Unit
        Execution is pipelined with 1 instr fed in each cycle
        latency of FU is as mentioned in config.py
    '''
    def __init__(self, latency):
        self.latency = latency
        '''
            InstrIdx => Reorder Buffer index, RegVal => value to be written to RenameReg & forwarded
            opCode: 1 => add, 0 => sub
        '''
        self.stages = []
        for _ in range(self.latency):
            temp = fuEntry(-1, None, -1)
            self.stages.extend([temp])

    def shiftAndEval(self, index= -1, opCode= -1, op1=None, op2=None):
        '''
            Note: If the RS is full, issue a NOP (so that the output value is got)
                  by passing the default values to shiftAndEval()
        '''
        out = self.stages[-1]
        self.stages[1:] = self.stages[0:-1]     # shift (pipelined exec)
        if (opCode == -1):      # NOP bubble
            regval = None
        else:
            if opCode == 'DIV':
                regval = op1/op2
            else:
                index = -1
                regval = None
        self.stages[0] = fuEntry(index, regval, opCode)
        return out

class LSU:
    '''
        Load/Store Functional Unit
        Unlike othger FUs, the LSU is not pipelined
    '''
    def __init__(self, latency):
        self.latency = latency
        self.dict = {'InstrIdx': -1, 'RegVal': None, 'opCode': -1, 'busy': 0}
        self.end = None

    def IssueNewOp(self, start, index= -1, opCode= -1, op1=None, op2=None, offset= None):
        '''
            Check if FU is busy before calling this Function
            Redundant "if(busy)" added
        '''
        if (self.dict['busy']):
            return 1       # busy, try again in next cycle
        else:
            if (opCode == -1):      # NOP bubble
                regval = None
                busy = 0
            else:
                busy = 1
                self.end = start + self.latency
                if opCode == 'LOD':
                    addr = (op1 + op2)%len(mem)
                    regval = mem[addr]
                elif opCode == 'STO':
                    regval = None
                    addr = (op2 + offset)%len(mem)
                    mem[addr] = op1
                else:
                    regval = None
                    index = -1
                    busy = 0
            self.dict = {'InstrIdx': index, 'RegVal': regval, 'opCode': opCode, 'busy': busy}
            return 0

    def pollLSU(self, clkVal):
        if(self.dict['busy']):
            if(clkVal == self.end):
                self.dict['busy'] = 0
                return self.dict
        return None

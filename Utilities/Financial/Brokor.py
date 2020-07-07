import numpy
import os,sys

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine):
        self.TimeLine = TimeLine
        self.DataLength = len(TimeLine)
        self.DataRange = [0, self.DataLength-1]
        self.Pointer = 0
        self.ModuleList = []
        self.Result = {}

        self.Data = {}
        self.OperationPoint = {}
        
        self.g = self.GetData
        self.t = self.GetDate
        self.j = self.Judge
    
    def RequireData(self, DataName):
        for Name in DataName:
            if Name not in self.Data:
                print('Require Data: ', Name)
                return False
        return True

    def GetData(self, DataName, Shift=-99999):
        if Shift == -99999:
            return self.Data[DataName]
        else:
            return self.Data[DataName][self.Pointer+Shift]
    
    def GetDate(self, Shift):
        return self.TimeLine[self.Pointer+Shift]
    
    def GetEmptyList(self):
        return [None]*(self.DataRange[0]+1)

    def ProvideData(self, Data):
        for Item in Data:
            if len(Data[Item]) == self.DataLength:
                Counter = -1
                for Member in (Data[Item]):
                    if numpy.isnan(Member):
                        Counter+=1
                    else:
                        break
                if Counter > self.DataRange[0]:
                    self.DataRange[0] = Counter
                self.Data[Item] = Data[Item]
            else:
                print(str(Item), ': Data Not Enough')

    def GetTimeRange(self):
        return [self.TimeLine[0], self.TimeLine[-1]]

    def LoadModule(self, Module):
        self.ModuleList.append(Module)

    def Traversal(self, Function, LeftMargin=0, RightMargin=0):
        self.Pointer = self.DataRange[0]
        self.PointerMargin = [self.DataRange[0]+LeftMargin, self.DataRange[1]-RightMargin]
        while True:
            ExitCode = Function(self)
            self.Pointer += 1
            if ExitCode or self.Pointer > self.PointerMargin[1]:
                break
    
    def Judge(self, JudgeList):
        if not JudgeList.count(False):
            return True
        return False

    def Run(self):
        for Module in self.ModuleList:
            Module.Run(self)
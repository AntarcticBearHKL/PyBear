import numpy
import os,sys

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine):
        self.TimeLine = TimeLine
        self.DataLength = len(TimeLine)
        self.Data = {}
        self.Pointer = 0
        self.ModuleList = []
    
    def RequireData(self, DataName):
        for Name in DataName:
            if Name not in self.Data:
                print('Require Data: ', Name)
                return False
        return True

    def GetData(self, DataName):
        return self.Data[DataName]

    def ProvideData(self, Data):
        for Item in Data:
            if len(Data[Item]) == self.DataLength:
                self.Data[Item] = Data[Item]

    def GetTimeRange(self):
        return [self.TimeLine[0], self.TimeLine[-1]]

    def LoadModule(self, Module):
        self.ModuleList.append(Module)

    def Traversal(self, Function, LeftMargin=0, RightMargin=0):
        self.Pointer = 0
        self.PointerMargin = [LeftMargin, self.DataLength-1-RightMargin]
        while True:
            Function(self)
            self.Pointer += 1
            if self.Pointer<self.PointerMargin[0] or self.Pointer>self.PointerMargin[1]:
                break

    def Run(self):
        for Module in self.ModuleList:
            Module.Run(self)
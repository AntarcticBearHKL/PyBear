import numpy
import os,sys

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self):
        self.TimeLine = None
        self.Pointer = 0

        self.ModuleList = []

        self.Data = {}
        self.Result = {}
        self.Recommended = False
        self.RecommendON = False
        
        self.g = self.GetData
        self.d = self.GetDate
        self.j = self.Judge
        self.r = self.Result
    

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
    
    def ProvideData(self, Data):
        if not self.TimeLine:
            return
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

    
    def GetDate(self, Shift=0):
        return self.TimeLine[self.Pointer+Shift]
    

    def GetEmptyList(self):
        return [None]*(self.DataRange[0]+1)


    def SetTimeLine(self, TimeLine):
        self.TimeLine = TimeLine
        self.DataLength = len(TimeLine)
        self.DataRange = [0, self.DataLength-1]
    
    def SetTime(self, Date):
        self.Pointer = self.TimeLine.index(Date)
            

    def GetTimeRange(self):
        return [self.TimeLine[0], self.TimeLine[-1]]

    def Process(self, Module):
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
        for JudgeItem in JudgeList:
            if JudgeItem.count(False) == 0:
                return True
        return False

    def Recommend(self):
        if self.RecommendON:
            self.Recommended = True

    def Run(self):
        for Module in self.ModuleList:
            Module.Run(self)
            self.Traversal(Module.TraversalFunction, LeftMargin=Module.LeftMargin, RightMargin=Module.RightMargin)


class BrokorProcedure:
    def __init__(self):
        self.LeftMargin = 0
        self.RightMargin = 0

    def Run(self):
        pass

    def TraversalFunction(self, b):
        pass
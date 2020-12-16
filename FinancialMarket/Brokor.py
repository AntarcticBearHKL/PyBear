import numpy
import os,sys
import json

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self):
        self.TimeLine = None
        self.Pointer = 0

        self.ModuleList = []

        self.Data = {}
        self.Result = {
            'Error': False,
            'ErrorIn': None,
            'ErrorLog': '',
        }
        self.Recommended = False
        
        self.d = self.GetData
        self.t = self.GetTime
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

    
    def SetTimeLine(self, TimeLine):
        self.TimeLine = TimeLine
        self.DataLength = len(TimeLine)
        self.DataRange = [0, self.DataLength-1]

    def GetTime(self, Shift=0):
        return self.TimeLine[self.Pointer+Shift]

    def GetTimeRange(self):
        return [self.TimeLine[0], self.TimeLine[-1]]

    
    def SetPointer(self, Date):
        self.Pointer = self.TimeLine.index(Date)


    def NewEmptyList(self, Name, Margin):
        self.Data[Name] = [None] * (self.DataRange[0] + 1 + Margin)

    def NewResult(self, Name):
        self.Result[Name] = []

    
    def Traversal(self, Function, LeftMargin=0, RightMargin=0):
        self.Pointer = self.DataRange[0] + LeftMargin + 1
        self.PointerMargin = [self.DataRange[0]+LeftMargin+1, self.DataRange[1]-RightMargin]
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
        self.Recommended = True


    def Process(self, Module):
        self.ModuleList.append(Module)


    def Run(self):
        for Module in self.ModuleList:
            Module.Brokor = self
            Module.Run()
            self.Traversal(Module.TraversalFunction, LeftMargin=Module.LeftMargin, RightMargin=Module.RightMargin)
            continue
            try:
                Module.Brokor = self
                Module.Run()
                self.Traversal(Module.TraversalFunction, LeftMargin=Module.LeftMargin, RightMargin=Module.RightMargin)
            except Exception as e:
                print(e)
                self.Result['Error']= True
                self.Result['ErrorIn']= Module
                self.Result['ErrorLog']= str(e)

    
    def PrintData(self, Filter=None):
        if Filter:
            pass
        for Counter in range(len(self.TimeLine)):
            Ret = {}
            for Item in self.Data:
                if Filter:
                    if Item in Filter:
                        Ret[Item] = self.Data[Item][Counter]
                else:
                    Ret[Item] = self.Data[Item][Counter]
            print(self.TimeLine[Counter], ': ', Ret)


class BrokorProcedure:
    def __init__(self, Config={}):
        self.LeftMargin = 0
        self.RightMargin = 0
        self.Config = Config


    def GetConfig(self, Name, Default=None):
        if Name in self.Config:
            return self.Config[Name]
        if Default != None:
            return Default
        raise GlobalBear.BadBear('No Config '+Name)

    def GetConfigInt(self, Name, Default=None):
        if Name in self.Config:
            return int(self.Config[Name])
        if Default != None:
            return int(Default)
        raise GlobalBear.BadBear('No Config '+Name)


    def Input(self, Name):
        if self.Brokor.RequireData([Name]):
            return self.Brokor.GetData(Name)
        else:
            raise GlobalBear.BadBear('No Data '+Name)

    def CheckInput(self, Name):
        if self.Brokor.RequireData([Name]):
            return True
        return False

    def Output(self, Name, Data):
        self.Brokor.ProvideData({Name: Data})

    def Run(self):
        pass

    def TraversalFunction(self, b):
        pass
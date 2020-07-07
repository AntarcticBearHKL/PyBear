import numpy
import os,sys

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine):
        self.TimeLine = TimeLine
        self.DataLimit = len(TimeLine)
        self.Data = {}

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
            self.Data[Item] = Data[Item]

    def GetTimeRange(self):
        return [self.TimeLine[0], self.TimeLine[-1]]

    def LoadModule(self, Strategy):
        Strategy.Execute(self)
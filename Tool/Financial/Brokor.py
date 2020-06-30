import numpy
import os,sys

import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine, Data, LeftMargin=0, RightMargin=0):
        os.system("cls")
        self.TimeLine = TimeLine
        self.Data = Data
        self.LastCommand=None

        self.CommandList = {}

        for Item in Data:
            if len(Data[Item]) != len(TimeLine):
                raise BadBear('Broker Data Not Synchronous')

        self.TimeLineIndex = {}
        IndexNumber = 0
        for Item in TimeLine:
            self.TimeLineIndex[Item] = IndexNumber
            IndexNumber += 1

        MinList = []
        MaxList = []
        for Item in Data:
            CounterList = []
            for Counter in range(len(Data[Item])):
                if Data[Item][Counter] == None or numpy.isnan(Data[Item][Counter]):
                    continue
                CounterList.append(Counter)
            MinList.append(min(CounterList))
            MaxList.append(max(CounterList))

        self.PointerMargin = [max(MinList) + LeftMargin, min(MaxList) - RightMargin]
        self.DataMargin = [max(MinList), min(MaxList)]

        if self.PointerMargin[0] > self.PointerMargin[1]:
            raise BadBear('Broker Data Not Enough')
        self.Pointer = self.PointerMargin[0]

    def LoadCommand(self, Package):
        Package.Load(self)

    def RunCommandBackground(self, Command):
        CommandDict = {}
        for Line in Command:
            Line = Line.split(' ')
            CommandDict[Line[0]] = Line[1:]
        
    def RunCommand(self, Command):
        CommandRaw = Command.split(' ')
        if CommandRaw[0].upper() in self.CommandList:
            self.LastCommand = Command
            self.CommandList[CommandRaw[0].upper()](CommandRaw[1:])
        else:
            print('UNKNOWN COMMAND')
            input('PRESS BUTTON TO CONTINUE...')

    def Run(self):
        print('-------------------------------')
        input('SYSTEM READY. PRESS BUTTON TO START...')
        while True:
            os.system("cls")
            print('TODAY IS:', self.TimeLine[self.Pointer])
            if self.Pointer > self.PointerMargin[1]:
                return
            Command = input('Command: ')
            if Command=='' and self.LastCommand:
                self.RunCommand(self.LastCommand)
            else:
                self.RunCommand(Command)

class BrokorCommand():
    def Init(self, Brokor):
        self.Brokor = Brokor
        print('-------------------------------')
        try:
            print('Loding Command: ', self.Name[0].upper())
            for Name in self.Name:
                self.Brokor.CommandList[Name.upper()] = self.CommandFunction
        except Exception as e:
            print('Loading Command Error')

    def CommandFunction(self, ParameterList):
        pass
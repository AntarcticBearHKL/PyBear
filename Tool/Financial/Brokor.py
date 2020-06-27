import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine):
        self.ModuleList = []
        self.LeftMarginList = []
        self.RightMarginList = []
        self.DataList = {}
        self.StrategyList = []
        self.FunctionList = []

    def LoadModule(self, Module):
        self.ModuleList.append(Module)

    def InitEnv(self):
        for Module in self.ModuleList:
            Module.Module.Run()

        for Strategy in StrategyList:
                Strategy.Run()
        self.TimeLine = TimeLine
        self.Data = Data

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

        self.StartPointer = max(MinList) + LeftMargin
        self.EndPointer = min(Max nm List) - RightMargin
        self.DataStartPointer = max(MinList)
        self.DataEndPointer = min(MaxList)
        if self.StartPointer > self.EndPointer:
            raise BadBear('Broker Data Not Enough')
        self.Pointer = self.StartPointer - 1 


    def Run(self):
        self.InitEnv()
        while True:
            os.system("cls")
            self.Pointer += 1
            if self.Pointer > self.EndPointer:
                return
            for Command in CommandList:
                Command.Check()
            input('PRESS ENTER TO CONTINUE...')

class BrokorModule():
    def __init__(self):
        pass

    def Data(self):
        pass

    def Strategy(self):
        pass

    def Command(self):
        pass
import PyBear.GlobalBear as GlobalBear

class Brokor:
    def __init__(self, TimeLine, Data, LeftMargin=0, RightMargin=0):
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
        self.EndPointer = min(MaxList) - RightMargin
        self.DataStartPointer = max(MinList)
        self.DataEndPointer = min(MaxList)
        if self.StartPointer > self.EndPointer:
            raise BadBear('Broker Data Not Enough')
        self.Pointer = self.StartPointer - 1 

    def __len__(self):
        return self.EndPointer - self.StartPointer + 1
    
    def GetData(self, Shift):
        if self.Pointer+Shift < self.DataStartPointer or self.Pointer+Shift > self.DataEndPointer:
            raise GlobalBear.BadBear('Beyond The Reach')
        Ret = {}
        for Item in self.Data:
            Ret[Item] = self.Data[Item][self.Pointer+Shift]
        return Ret

    def Start(self, Func):
        while True:
            os.system("cls")
            self.Pointer += 1
            if self.Pointer > self.EndPointer:
                return
            Func(self)
            input('PRESS ENTER TO CONTINUE...')
import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Market as MarketBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        Data = MarketBear.CHN.Stock(self.GetConfig('StockCode')).GetPrice(Day=self.GetConfigInt('Day', '120'))
        if len(Data) != self.GetConfigInt('Day', '120'):
            raise GlobalBear.BadBear('Not Enough Trade Day')
        TimeLine = []
        OpenList = []
        HighList = []
        LowList = []
        CloseList = []
        VolList = []
        AmountList = []

        for Item in Data:
            TimeLine.append(Item['Date'])
            OpenList.append(Item['Open'])
            HighList.append(Item['High'])
            LowList.append(Item['Low'])
            CloseList.append(Item['Close'])
            VolList.append(Item['Volumn'])
            AmountList.append(Item['Amount'])

        self.Brokor.SetTimeLine(TimeLine)

        self.Output('Open', OpenList)
        self.Output('High', HighList)
        self.Output('Low', LowList)
        self.Output('Close', CloseList)
        self.Output('Vol', VolList)
        self.Output('Amount', AmountList)
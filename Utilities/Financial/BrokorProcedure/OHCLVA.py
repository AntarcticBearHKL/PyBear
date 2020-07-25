import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Market as MarketBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        print('ajjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        TimeRange = MarketBear.CHN.StockMarket().GetTradeDayRange(Day=self.GetConfig('Day', '120'))
        Data = MarketBear.CHN.Stock(self.GetConfig('StockCode')).GetPrice(TimeRange)
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
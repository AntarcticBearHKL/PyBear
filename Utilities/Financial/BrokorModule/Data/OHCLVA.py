import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Market as MarketBear

class Config:
    def __init__(self, StockCode, Day=120):
        self.StockCode = StockCode
        self.Day = Day

    def Run(self, Brokor):
        TimeRange = MarketBear.CHN.StockMarket().GetTradeRange(Day=self.Day)
        Data = MarketBear.CHN.Stock(self.StockCode).GetPrice(TimeRange)
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

        Brokor.SetTimeLine(TimeLine)

        Brokor.ProvideData({
            'Open': OpenList,
            'High': HighList,
            'Low': LowList,
            'Close': CloseList,
            'Vol': VolList,
            'Amount': AmountList})
import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Market as MarketBear

class Config:
    def __init__(self, StockCode=None):
        self.StockCode = StockCode 

    def Run(self, Brokor):
        if not self.StockCode:
            print('OHCLVA No StockCode')
            return

        TimeRange = Brokor.GetTimeRange()
        Data = MarketBear.CHN.Stock(self.StockCode).GetPrice(TimeRange)
        OpenList = []
        HighList = []
        LowList = []
        CloseList = []
        VolList = []
        AmountList = []

        for Item in Data:
            OpenList.append(Item['Open'])
            HighList.append(Item['High'])
            LowList.append(Item['Low'])
            CloseList.append(Item['Close'])
            VolList.append(Item['Volumn'])
            AmountList.append(Item['Amount'])

        Brokor.ProvideData({
            'Open': OpenList,
            'High': HighList,
            'Low': LowList,
            'Close': CloseList,
            'Vol': VolList,
            'Amount': AmountList})
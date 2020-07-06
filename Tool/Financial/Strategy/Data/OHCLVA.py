import PyBear.GlobalBear as GlobalBear
import PyBear.Tool.Financial.Market as MarketBear

def Execute(Brokor):
    if not Brokor.RequireData(['StockCode']):
        return

    TimeRange = Brokor.GetTimeRange()
    Data = MarketBear.CHN.Stock(Brokor.GetData('StockCode')).GetPrice(TimeRange)
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
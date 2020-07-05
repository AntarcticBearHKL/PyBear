import PyBear.GlobalBear as GlobalBear
import PyBear.Tool.Financial.Market as MarketBear

def Execute(Brokor):
    Brokor.RequireData([])

    TimeRange = Brokor.GetTimeRange()
    Data = MarketBear.CHN.Stock(StockCode).GetPrice(TimeRange[0], TimeRange[1])
    
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
        VolList.append(Item['Vol'])
        AmountList.append(Item['Amount'])

    Brokor.ProvideData({'Open': OpenList})
    Brokor.ProvideData({'High': HighList})
    Brokor.ProvideData({'Low': LowList})
    Brokor.ProvideData({'Close': CloseList})
    Brokor.ProvideData({'Vol': VolList})
    Brokor.ProvideData({'Amount': AmountList})
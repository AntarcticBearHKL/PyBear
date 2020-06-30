import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Tool.Financial.Market as MarketBear
import PyBear.Tool.Financial.Quantification as QuantificationBear
import PyBear.Library.Statistics as StatisticsBear

def Run(End=None):
    TM = MultitaskBear.TaskMatrix(12,8)

    CHNStockMarket = MarketBear.CHN.StockMarket().Init()
    if not End:
        End = CHNStockMarket.LastTradeDay()
    StrategyName = str(End) + '_CoreStrategy'
    RedisBear.Redis('RedisLocal').delete(StrategyName)

    Date = CHNStockMarket.GetTradeDay(End=End, Day=120)

    StockArg = [[Item, Date[0], Date[-1], StrategyName] for Item in CHNStockMarket.GetStockCode(TSCode=True, Filter=['SZ', 'SH', 'ZX'])]
    print('Ready To Launch')
    TM.ImportTask(Workload, StockArg)
    TM.Start()

def Workload(StockCode, Start, End, DBName):
    ErrorCounter = 0
    while True:
        try:   
            Price = MarketBear.CHN.Stock(StockCode).GetRange(Start, End)
            Close = [Item['Close'] for Item in Price]
            DIF, DEA, MACD = QuantificationBear.MACD(Close)
            if \
            (DIF[-2]<0 and DIF[-1]>0) and\
            DEA[-1]<0:
                RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), str(StatisticsBear.Std(Close[-60:-1])))

            print(StockCode)
            break
        except Exception as e:
            ErrorCounter +=1
            print(StockCode, ': Error(' + str(ErrorCounter) +')')
            if ErrorCounter >= 10:
                RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                break
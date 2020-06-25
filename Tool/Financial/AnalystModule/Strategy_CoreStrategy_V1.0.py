
def StrategyMACD(End=None):
    TM = MultitaskBear.TaskMatrix(12,8)

    CHNStockMarket = CHN.StockMarket().Init()
    if not End:
        End = CHNStockMarket.LastTradeDay()
    StrategyName = str(End) + '_StrategyMACD_V1'
    RedisBear.Redis('RedisLocal').delete(StrategyName)

    Date = CHNStockMarket.GetTradeDay(End=End, Day=120)

    StockArg = [[Item, Date[0], Date[-1], StrategyName] for Item in CHNStockMarket.GetStockCode(TSCode=True, Filter=['SZ', 'SH'])]
    print('Ready To Launch')
    TM.ImportTask(WorkLoad.StrategyMACD, StockArg)
    TM.Start()

    print('----------------------------------')
    Analyst.LogCheck(StrategyName)

def StrategyMACD(StockCode, Start, End, DBName):
    ErrorCounter = 0
    while True:
        try:   
            Price = CHN.Stock(StockCode).GetRange(Start, End)
            PriceList = [Item['Close'] for Item in Price]
            Upper, Middle, Lower = Quantification.BOLL(PriceList)
            DIF, DEA, MACD = Quantification.MACD(PriceList)
            if \
            ( DIF[-1]>0 and DEA[-1]>0 and MACD[-1]>0 ) and \
            ( DIF[-2]<0 or DEA[-2]<0 or MACD[-2]<0 ) and \
            ( DIF[-3]<0 or DEA[-3]<0 or MACD[-3]<0 ) and \
            ( MACD[-1]>MACD[-2] and MACD[-2]>MACD[-3] ) and \
            ( PriceList[-1]<Middle[-1] ):
                RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), str(StatisticsBear.Std(PriceList[-60:-1])))

            print(StockCode)
            break
        except Exception as e:
            ErrorCounter +=1
            print(StockCode, ': Error(' + str(ErrorCounter) +')')
            if ErrorCounter >= 10:
                RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                break
import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Tool.Financial.Market as MarketBear

def Run():
    LimitPerMinute = int(input('Update CHN Stock Limit Per Minute: '))
    LimitPerMinute = int(LimitPerMinute/2)
    TM = MultitaskBear.TaskMatrix(2,32, LimitPerMinute=LimitPerMinute)

    CHNStockMarket = MarketBear.CHN.StockMarket().Init()
    LastTradeDay = CHNStockMarket.LastTradeDay()
    RedisBear.Redis('RedisLocal').delete('DailyUpdate')

    StockArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
    print('Ready To Launch')
    TM.ImportTask(Workload, StockArg)
    TM.Start()

def Workload(StockCode, LastTradeDay):
    ErrorCounter = 0
    while True:
        try:
            print(StockCode)
            Ret = MarketBear.CHN.Stock(StockCode).Sync(LastTradeDay)
            RedisBear.Redis('RedisLocal').hset('DailyUpdate', StockCode, str(Ret))
            break
        except Exception as e:
            ErrorCounter +=1
            print(StockCode, ': Error(' + str(ErrorCounter) +')')
            if ErrorCounter >= 10:
                RedisBear.Redis('RedisLocal').hset('DailyUpdate', StockCode, 'Error: ' + str(e))
                break
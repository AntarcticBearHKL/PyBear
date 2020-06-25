import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear

def Workload(LimitPerMinute=None):
    TM = MultitaskBear.TaskMatrix(2,32, LimitPerMinute=LimitPerMinute)

    CHNStockMarket = CHN.StockMarket().Init()
    LastTradeDay = CHNStockMarket.LastTradeDay()
    RedisBear.Redis('RedisLocal').delete('DailyUpdate')

    StockArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
    print('Ready To Launch')
    TM.ImportTask(Workload, StockArg)
    TM.Start()

    print('----------------------------------')
    Analyst.LogCheck('DailyUpdate')

def Workload(StockCode, LastTradeDay):
    ErrorCounter = 0
    while True:
        try:
            Ret = CHN.Stock(StockCode).Sync(LastTradeDay)
            RedisBear.Redis('RedisLocal').hset('DailyUpdate', StockCode, str(Ret))
            break
        except Exception as e:
            ErrorCounter +=1
            print(StockCode, ': Error(' + str(ErrorCounter) +')')
            if ErrorCounter >= 10:
                RedisBear.Redis('RedisLocal').hset('DailyUpdate', StockCode, 'Error: ' + str(e))
                break
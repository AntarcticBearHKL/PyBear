import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Utilities.Financial.Market as MarketBear

class Config:
    def __init__(self, LimitPerMinute=700):
        self.LimitPerMinute = LimitPerMinute

    def Run(self):
        LimitPerMinute = int(self.LimitPerMinute/2)
        TM = MultitaskBear.TaskMatrix(2,32, LimitPerMinute=LimitPerMinute)

        CHNStockMarket = MarketBear.CHN.StockMarket().CheckUpdate()
        LastTradeDay = CHNStockMarket.LastTradeDay()
        RedisBear.Redis('RedisLocal').delete('DailyUpdate')

        StockArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
        print('Ready To Launch')
        TM.ImportTask(self.ThreadFunction, StockArg)
        TM.Start()

    def ThreadFunction(self, StockCode, LastTradeDay):
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
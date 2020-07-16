import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Utilities.Financial.Market as MarketBear
import PyBear.Utilities.Financial.Analyst as AnalystBear

class Config(AnalystBear.AnalystModule):
    def __init__(self, LimitPerMinute=700):
        self.LimitPerMinute = LimitPerMinute

    def Run(self):
        LimitPerMinute = int(self.LimitPerMinute/2)
        TM = MultitaskBear.TaskMatrix(2,32, LimitPerMinute=LimitPerMinute)

        CHNStockMarket = MarketBear.CHN.StockMarket().Update()
        LastTradeDay = CHNStockMarket.GetTradeDay(Day=1)[0]

        RedisBear.Redis('RedisLocal').delete('CHNStockAndIndexUpdate')

        StockArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetStockCode()]
        IndexArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetIndexCode()]
        print('READY TO LAUNCH...')
        TM.ImportTask(self.UpdateStock, StockArg)
        TM.ImportTask(self.UpdateIndex, IndexArg)
        TM.Start()

    def UpdateStock(self, StockCode, LastTradeDay):
        ErrorCounter = 0
        while True:
            try:
                MarketBear.CHN.Stock(StockCode).Sync(LastTradeDay)
                RedisBear.Redis('RedisLocal').hset('CHNStockAndIndexUpdate', StockCode, 'Finish')
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    RedisBear.Redis('RedisLocal').hset('CHNStockAndIndexUpdate', StockCode, 'Error: ' + str(e))
                    break
    
    def UpdateIndex(self, IndexCode, LastTradeDay):
        ErrorCounter = 0
        while True:
            try:
                Ret = MarketBear.CHN.Index(IndexCode).Sync(LastTradeDay)
                RedisBear.Redis('RedisLocal').hset('CHNStockAndIndexUpdate', IndexCode, 'Finish')
                break
            except Exception as e:
                ErrorCounter +=1
                print(IndexCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    RedisBear.Redis('RedisLocal').hset('CHNStockAndIndexUpdate', IndexCode, 'Error: ' + str(e))
                    break
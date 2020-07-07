import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Tool.Financial.Market as MarketBear
import PyBear.Tool.Financial.Quantification as QuantificationBear
import PyBear.Library.Statistics as StatisticsBear

class Config:
    def __init__(self, EndDay=None):
        self.EndDay = EndDay

    def Run(self):
        TM = MultitaskBear.TaskMatrix(12,8)

        CHNStockMarket = MarketBear.CHN.StockMarket().CheckUpdate()
        if not self.EndDay:
            self.EndDay = CHNStockMarket.LastTradeDay()
        StrategyName = str(self.EndDay) + '_CoreStrategy'
        RedisBear.Redis('RedisLocal').delete(StrategyName)

        Date = CHNStockMarket.GetTradeDay(End=self.EndDay, Day=120)

        StockArg = [[Item, Date[0], Date[-1], StrategyName] for Item in CHNStockMarket.GetStockCode(TSCode=True, Filter=['SZ', 'SH', 'ZX'])]
        print('Ready To Launch')
        TM.ImportTask(self.Workload, StockArg)
        TM.Start()

    def Workload(self, StockCode, Start, End, DBName):
        ErrorCounter = 0
        while True:
            try:   
                Price = MarketBear.CHN.Stock(StockCode).GetPrice([Start, End])
                MID = [(Item['Close']+Item['Open'])/2 for Item in Price]
                DIF, DEA, MACD = QuantificationBear.MACD(MID)
                if \
                (DIF[-2]<0 and DIF[-1]>0) and\
                DEA[-1]<0:
                    RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), str(StatisticsBear.Std(MID[-60:-1])))

                print(StockCode)
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                    break
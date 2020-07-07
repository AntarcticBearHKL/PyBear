import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Utilities.Financial.Market as MarketBear    
import PyBear.Utilities.Financial.Brokor as BrokorBear

import PyBear.Utilities.Financial.BrokorModule.Data.OHCLVA as OHCLVA
import PyBear.Utilities.Financial.BrokorModule.Quantification.MACD as MACD
import PyBear.Utilities.Financial.BrokorModule.Quantification.BOLL as BOLL
import PyBear.Utilities.Financial.BrokorModule.Quantification.KDJ as KDJ
import PyBear.Utilities.Financial.BrokorModule.Quantification.RSI as RSI
import PyBear.Utilities.Financial.BrokorModule.OperationPoint.StrategyAlpha as StrategyAlpha

class Config:
    def __init__(self):
        self.StrategyName = ChronusBear.Date().String(-1) + '_CoreStrategy'

    def Run(self):
        #TM = MultitaskBear.TaskMatrix(12,8)
        TM = MultitaskBear.TaskMatrix(1,1)

        CHNStockMarket = MarketBear.CHN.StockMarket().CheckUpdate()
        RedisBear.Redis('RedisLocal').delete(self.StrategyName)

        TimeRange = CHNStockMarket.GetTradeDay(Day=120)

        StockArg = [[Item, TimeRange, self.StrategyName] for Item in CHNStockMarket.GetStockCode(TSCode=True, Filter=['SZ', 'SH', 'ZX'])]
        print('Ready To Launch')
        TM.ImportTask(self.Workload, StockArg)
        TM.Start()

    def Workload(self, StockCode, TimeRange, DBName):
        ErrorCounter = 0
        while True:
            try:
                Brokor = BrokorBear.Brokor(TimeRange)
                Brokor.LoadModule(OHCLVA.Config(StockCode=StockCode))
                Brokor.LoadModule(MACD.Config())
                Brokor.LoadModule(BOLL.Config())
                Brokor.LoadModule(KDJ.Config())
                Brokor.LoadModule(RSI.Config())
                Brokor.LoadModule(StrategyAlpha.Config())
                Brokor.Run()
                if Brokor.Result['StrategyAlpha'][-1] == 1: 
                    RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), 'Success')
                print(StockCode)
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                    break
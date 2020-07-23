import PyBear.GlobalBear as GlobalBear

import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear
import PyBear.Utilities.Financial.Market as MarketBear    
import PyBear.Utilities.Financial.Brokor as BrokorBear
import PyBear.Utilities.Financial.Analyst as AnalystBear

import PyBear.Utilities.Financial.BrokorProcedure.OHCLVA as OHCLVA
import PyBear.Utilities.Financial.BrokorProcedure.MACD as MACD
import PyBear.Utilities.Financial.BrokorProcedure.BOLL as BOLL
import PyBear.Utilities.Financial.BrokorProcedure.KDJ as KDJ
import PyBear.Utilities.Financial.BrokorProcedure.RSI as RSI
import PyBear.Utilities.Financial.BrokorProcedure.StrategyAlpha as StrategyAlpha

class Config(AnalystBear.AnalystProcedure):
    def __init__(self):
        self.StrategyName = 'CoreStrategy_' + input('Enter Strategy Result Name:') + '_' + str(CipherBear.NumberIndex())

    def Run(self):
        TM = MultitaskBear.TaskMatrix(12,8)

        RedisBear.Redis('RedisLocal').delete(self.StrategyName)

        StockArg = [[Item, self.StrategyName] for Item in MarketBear.CHN.StockMarket().Update().GetStockCode(Filter=['SZ', 'SH', 'ZX', 'CY'])]
        print('READY TO LAUNCH...')
        TM.ImportTask(self.Workload, StockArg)
        TM.Start()

    def Workload(self, StockCode, DBName):
        ErrorCounter = 0
        while True:
            try:
                Brokor = BrokorBear.Brokor()
                Brokor.LoadModule(OHCLVA.Config(StockCode=StockCode))
                Brokor.LoadModule(MACD.Config())
                Brokor.LoadModule(BOLL.Config())
                Brokor.LoadModule(KDJ.Config())
                Brokor.LoadModule(RSI.Config())
                Brokor.LoadModule(StrategyAlpha.Config())
                Brokor.Run()

                if Brokor.Recommended:
                    RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), 'Success')
                print(StockCode)
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 5:
                    RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                    break

    def Portfolio(self):
        Keys = RedisBear.Redis('RedisLocal').hgetall(self.StrategyName)
        Keylist = list(Keys)
        Keylist.sort()
        for Key in Keylist:
            print(Key, ': ', Keys[Key])
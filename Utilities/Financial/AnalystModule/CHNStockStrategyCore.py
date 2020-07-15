import PyBear.GlobalBear as GlobalBear

import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear
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
        self.StrategyName = 'CoreStrategy_' + str(CipherBear.NumberIndex) + '_'

    def Run(self):
        self.StrategyName += input('Enter Strategy Result Name:')
        TM = MultitaskBear.TaskMatrix(12,8)

        RedisBear.Redis('RedisLocal').delete(self.StrategyName)

        StockArg = [[Item, self.StrategyName] for Item in MarketBear.CHN.StockMarket().CheckUpdate().GetStockCode(TSCode=True, Filter=['SZ', 'SH', 'ZX', 'CY'])]
        print('Ready To Launch')
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
                
                if Ret[-1]!=None:
                    RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), str(Ret[-1]))
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
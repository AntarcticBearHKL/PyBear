import PyBear.GlobalBear as GlobalBear

import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Data.Redis as RedisBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Utilities.Financial.Market as MarketBear    
import PyBear.Utilities.Financial.Brokor as BrokorBear
import PyBear.Utilities.Financial.Analyst as AnalystBear

import PyBear.Utilities.Financial.BrokorProcedure.OHCLVA as OHCLVA
import PyBear.Utilities.Financial.BrokorProcedure.MACD as MACD
import PyBear.Utilities.Financial.BrokorProcedure.BOLL as BOLL
import PyBear.Utilities.Financial.BrokorProcedure.KDJ as KDJ
import PyBear.Utilities.Financial.BrokorProcedure.RSI as RSI
import PyBear.Utilities.Financial.BrokorProcedure.StrategyMACD as StrategyMACD
import PyBear.Utilities.Financial.BrokorProcedure.Recommander as Recommander

class Config(AnalystBear.AnalystProcedure):
    def __init__(self):
        self.StrategyName = 'CoreStrategy_' + input('Enter Strategy Result Name:')

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
                Brokor.Process(OHCLVA.Config({
                    'StockCode': StockCode,
                    'Day': '250'
                }))
                Brokor.Process(MACD.Config({
                    'Fast': '22',
                    'Slow': '120',
                    'Signal': '9'
                }))
                Brokor.Process(KDJ.Config({
                    'FastK': '22',
                    'SlowK': '3',
                    'SlowD': '3',
                }))
                Brokor.Process(StrategyMACD.Config({}))
                Brokor.Process(Recommander.Config({
                    'Target': 'StrategyMACD'
                }))
                Brokor.Run()

                if Brokor.Recommended:
                    print(StockCode, 'Success')
                    RedisBear.Redis('RedisLocal').hset(DBName, str(StockCode), 'Success')
                else:
                    print(StockCode, 'Failed')
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 2:
                    RedisBear.Redis('RedisLocal').hset(DBName, StockCode, 'Error: ' + str(e))
                    break

    def Portfolio(self):
        Keys = RedisBear.Redis('RedisLocal').hgetall(self.StrategyName)
        Keylist = list(Keys)
        Keylist.sort()
        for Key in Keylist:
            print(Key, ': ', Keys[Key])
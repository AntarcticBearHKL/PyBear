import os,sys
import tushare
import talib
import numpy
import pandas
import warnings
warnings.filterwarnings('ignore')

import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Statistics as StatisticsBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.Redis as RedisBear

class CHN:
    class MacroMarket:
        def __init__(self):
            pass

    class BondMarket:
        def __init__(self):
            pass

    class StockMarket:
        def __init__(self):
            try:
                tushare.set_token(GlobalBear.TushareToken)
            except:
                raise BadBear('Tushare Cannot Use Without Token')
            self.API = tushare.pro_api()

        def Update(self):
            print("CHECK TRADE DAY UPDATE...")
            self.UpdateTradeDay()
            print("CHECK STOCK BASIC UPDATE...")
            self.UpdateStockBasic()
            print("CHECK INDEX BASIC UPDATE...")
            self.UpdateIndexBasic()
            return self

        def UpdateStockBasic(self):
            StockBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'StockBasic')
            UpdateTime = StockBasicInfoTable.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                return


            print('STOCK BASIC UPDATE START...')
            StockBasicInfo = self.API.stock_basic()

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
            }]
            for Item in StockBasicInfo.itertuples():
                Data.append({
                    'Code': int(Item.symbol),
                    'TSCode': Item.ts_code,
                    'Name': Item.name,
                    'Area': Item.area,
                    'Industry': Item.industry,
                })
            
            StockBasicInfoTable.Delete({})
            StockBasicInfoTable.Insert(Data)
            print('STOCK BASIC UPDATE FINISH...')

        def UpdateIndexBasic(self):
            IndexBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'IndexBasic')
            UpdateTime = IndexBasicInfoTable.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                return

            print('INDEX BASIC UPDATE START...')
            IndexBasicInfo = self.API.index_basic()

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
            }]
            for Item in IndexBasicInfo.itertuples():
                Data.append({
                    'TSCode': Item.ts_code,
                    'Name': Item.name,
                    'Category': Item.category,
                })
            
            IndexBasicInfoTable.Delete({})
            IndexBasicInfoTable.Insert(Data)
            print('INDEX BASIC UPDATE FINISH...')

        def UpdateTradeDay(self):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            UpdateTime = TradeDayTable.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                return

            print('TRADE DAY UPDATE START...')
            EndDate = ChronusBear.Date()
            EndDate.SetTime(Month=12, Day=999)
            TradeDay = self.API.trade_cal(exchange='', start_date='20000101', end_date=EndDate.String(-1))

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
            }]
            for Item in TradeDay.itertuples():
                Data.append({
                    'Date': int(Item.cal_date),
                    'IsOpen': int(Item.is_open),
                })

            
            TradeDayTable.Delete({})
            TradeDayTable.Insert(Data)
            print('TRADE DAY UPDATE FINISH...')


        def GetStockCode(self, Filter=[]):
            StockBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'StockBasic')
            Condition = []
            if 'SZ' in Filter:
                Condition.append({
                    '$and': [
                        {'Code': {'$gte': 0}},
                        {'Code': {'$lte': 1000}},
                    ]
                })
            if 'ZX' in Filter:
                Condition.append({
                    '$and': [
                        {'Code': {'$gte': 2000}},
                        {'Code': {'$lte': 299999}},
                    ]
                })
            if 'CY' in Filter:
                Condition.append({
                    '$and': [
                        {'Code': {'$gte': 300000}},
                        {'Code': {'$lte': 599999}},
                    ]
                })
            if 'SH' in Filter:
                Condition.append({
                    '$and': [
                        {'Code': {'$gte': 600000}},
                        {'Code': {'$lte': 687000}},
                    ]
                })
            if 'KC' in Filter:
                Condition.append({
                    '$and': [
                        {'Code': {'$gte': 688000}},
                    ]
                })
            if len(Condition) != 0:
                Condition =  {'$or': Condition}
            else:
                Condition = {}
            Ret = StockBasicInfoTable.Search({
                '$and': [
                    {'TSCode': {'$exists': 'true'}},
                    Condition
                ]
            })
            return [Item['TSCode'] for Item in Ret]

        def GetIndexCode(self):
            IndexBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'IndexBasic')
            IndexList = IndexBasicInfoTable.Search({
                'TSCode': {'$exists': 'true'},
            })
            Ret = []
            for Index in IndexList:
                try:
                    int(Index['TSCode'][0])
                    Ret.append(Index['TSCode'])
                except:
                    pass
            return Ret


        def IsTradeDay(self, TestedDay):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            Ret = TradeDayTable.Search({
                'Date': TestedDay
            })
            if len(Ret) != 0 and Ret[0]['IsOpen'] == 1:
                return True
            return False

        def LatestTradeDay(self):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            if ChronusBear.Date().HourInt() <= 17:
                TargetDay = ChronusBear.Date().Shift(Day=-1).String(-1)
            else:
                TargetDay = ChronusBear.Date().String(-1)
            Ret = TradeDayTable.Search({
                'Date' : {'$lte': int(TargetDay)},
            }, Sort=['Date', -1], Limit=1)
            return Ret[0]['Date']


    class FundMarket:
        def __init__(self):
            try:
                tushare.set_token(GlobalBear.TushareToken)
            except:
                raise BadBear('Tushare Cannot Use Without Token')
            self.API = tushare.pro_api()
        
        def UpdateFundBasic(self):
            FundBasicInfo = MongoDBBear.MongoDB('MongoDB', 'FundCHN', 'FundBasicInfo')
            UpdateTime = FundBasicInfo.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                print('Update FundBasic Finish(N)')
                return


            print('Update FundBasic Start')
            BasicInfo = self.API.fund_basic()
            return BasicInfo

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
            }]
            for Item in BasicInfo.itertuples():
                Data.append({
                    'Code': int(Item.symbol),
                    'TSCode': Item.ts_code,
                    'Name': Item.name,
                    'Area': Item.area,
                    'Industry': Item.industry,
                })
            
            StockBasicInfoTable.Delete({})
            StockBasicInfoTable.Insert(Data)
            print('Update StockBasic Finish')


    class CommodityMarket:
        def __init__(self):
            pass

    class RealEstateMarket:
        def __init__(self):
            pass


    class Bond:
        def __init__(self):
            pass

    class Stock:
        def __init__(self, TSCode):
            try:
                tushare.set_token(GlobalBear.TushareToken)
            except:
                raise BadBear('Tushare Cannot Use Without Token')
            self.API = tushare.pro_api()
            self.TSCode = TSCode
             
            self.TickTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'Price_'+TSCode[0:6])


        def Sync(self, LastTradeDay):
            LastTradeDay = int(LastTradeDay)
            UpdateTime = self.TickTable.Search({},Sort=['Date', -1],Limit=1)
            if len(UpdateTime) != 0:
                if LastTradeDay > int(ChronusBear.Date(UpdateTime[0]['Date']).String(-1)):
                    return self.Update(Start=ChronusBear.Date(UpdateTime[0]['Date']).Shift(Day=1).String(-1), End=LastTradeDay)
                else:
                    print(self.TSCode, ": Don't Need Update")
                    return
            else:
                return self.Update(Start=999, End=LastTradeDay)

        def Update(self, Start, End):
            if Start == 999:
                Start = '20000101'
            Tick = tushare.pro_bar(ts_code = self.TSCode, adj='qfq', start_date=str(Start), end_date=str(End))
            if len(Tick) == 0:
                print(self.TSCode, ': Stock Is Dead')
                return

            Data = []
            for Item in Tick.itertuples():
                Data.append({
                    'TSCode': Item.ts_code,
                    'Date': int(Item.trade_date),
                    'Open': Item.open,
                    'High': Item.high,
                    'Low': Item.low,
                    'Close': Item.close,
                    'Volumn': Item.vol,
                    'Amount': Item.amount,
                })
            Data.reverse()
            self.TickTable.Insert(Data)
            print(self.TSCode, ': UPDATE ', str(len(Data)), ' Data')

        def GetPrice(self, Start=None, End=None, Day=None):
            if Start and End:  
                Ret = self.TickTable.Search({
                    '$and': [
                        { 'Date': {'$gte': int(Start)} },
                        { 'Date': {'$lte': int(End)}   },
                    ],
                }, Sort=['Date', 1])
                return Ret
            elif Start and Day:
                Ret = self.TickTable.Search({
                    'Date': {'$gte': int(Start)},
                }, Sort=['Date', 1], Limit=int(Day))
                return Ret
            elif End and Day:
                Ret = self.TickTable.Search({
                    'Date': {'$lte': int(End)}
                }, Sort=['Date', -1], Limit=int(Day))
                Ret.reverse()
                return Ret
            elif Day:
                if Day<0:
                    Ret = self.TickTable.Search({})
                    return Ret

                if ChronusBear.Date().HourInt() <= 17:
                    TargetDay = ChronusBear.Date().Shift(Day=-1).String(-1)
                else:
                    TargetDay = ChronusBear.Date().String(-1)
                    
                Ret = self.TickTable.Search({}, Sort=['Date', -1], Limit=int(Day))
                Ret.reverse()
                return Ret
            else:
                raise GlobalBear.BadBear('GetPrice Parameter Error')
   
    class Company:
        def __init__(self, TSCode):
            pass

    class Index:
        def __init__(self, TSCode):
            try:
                tushare.set_token(GlobalBear.TushareToken)
            except:
                raise BadBear('Tushare Cannot Use Without Token')
            self.API = tushare.pro_api()
            self.TSCode = TSCode
             
            self.TickTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'Price_Index_'+TSCode[0:6])


        def Sync(self, LastTradeDay):
            LastTradeDay = int(LastTradeDay)
            UpdateTime = self.TickTable.Search({},Sort=['Date', -1],Limit=1)
            if len(UpdateTime) != 0:
                if LastTradeDay > int(ChronusBear.Date(UpdateTime[0]['Date']).String(-1)):
                    return self.Update(Start=ChronusBear.Date(UpdateTime[0]['Date']).Shift(Day=1).String(-1), End=LastTradeDay)
                else:
                    print(self.TSCode, ": Don't Need Update")
                    return
            else:
                return self.Update(Start=999, End=LastTradeDay)

        def Update(self, Start, End):
            if Start == 999:
                Start = '20000101'
            Tick = self.API.index_daily(ts_code = self.TSCode, adj='qfq', start_date=str(Start), end_date=str(End))
            if len(Tick) == 0:
                print(self.TSCode, ': Index Is Dead')
                return

            Data = []
            for Item in Tick.itertuples():
                Data.append({
                    'TSCode': Item.ts_code,
                    'Date': int(Item.trade_date),
                    'Open': Item.open,
                    'High': Item.high,
                    'Low': Item.low,
                    'Close': Item.close,
                    'Volumn': Item.vol,
                    'Amount': Item.amount,
                })
            Data.reverse()
            self.TickTable.Insert(Data)
            print(self.TSCode, ': UPDATE ', str(len(Data)), ' Data')

        def GetPrice(self, TimeRange):
            Ret = self.TickTable.Search({
                '$and': [
                    {'Date': {'$gte': TimeRange[0]}},
                    {'Date': {'$lte': TimeRange[1]}}]
            })
            return Ret
   
        def GetTimeRange(self):
            Ret = [
                self.TickTable.Search({},Sort=['Date', 1],Limit=1)[0]['Date'],
                self.TickTable.Search({},Sort=['Date', -1],Limit=1)[0]['Date']]
            return Ret


    class Fund:
        def __init__(self):
            pass
     
    class Commodity:
        def __init__(self):
            pass

    class RealEstate:
        def __init__(self):
            pass

class HK:
    class StockMarket:
        def __init__(self):
            pass
    

    class Stock:
        def __init__(self):
            pass

class GLOBAL:
    class CurrencyMarket:
        def __init__(self):
            pass

    class DigitalCurrencyMarket:
        def __init__(self):
            pass


    class Currency:
        def __init__(self):
            pass

    class DigitalCurrency:
        def __init__(self):
            pass
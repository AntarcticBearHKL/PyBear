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

        def Init(self):
            self.UpdateStockBasic()
            self.UpdateTradeDay()
            return self

        def UpdateStockBasic(self):
            StockBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'StockBasic')
            UpdateTime = StockBasicInfoTable.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                print('Update StockBasic Finish(N)')
                return


            print('Update StockBasic Start')
            BasicInfo = self.API.stock_basic()

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

        def UpdateTradeDay(self):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            UpdateTime = TradeDayTable.Search({
                'UpdateTime': {'$exists': 'true'}
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                print('Update TradeDay Finish(N)')
                return

            print('Update TradeDay Start')
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
            print('Update TradeDay Finish')


        def GetStockCode(self, TSCode=None, Filter=[]):
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
                    {'Code': {'$exists': 'true'}},
                    Condition
                ]
            })
            if TSCode:
                return [Item['TSCode'] for Item in Ret]
            return [Item['Code'] for Item in Ret]


        def IsTradeDay(self, TestedDay):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            Ret = TradeDayTable.Search({
                'Date': TestedDay
            })
            if len(Ret) != 0 and Ret[0]['IsOpen'] == 1:
                return True
            return False

        def LastTradeDay(self):
            if ChronusBear.Date().HourInt() <= 17:
                TargetDay = ChronusBear.Date().Shift(Day=-1).String(-1)
            else:
                TargetDay = ChronusBear.Date().String(-1)
            
            return self.GetTradeDay(End=TargetDay, Day=1)[0] 

        def GetTradeDay(self, Start=None, End=None, Day=None):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            if Start and End:  
                Ret = TradeDayTable.Search({
                    '$and': [
                        { 'Date': {'$gte': int(Start)} },
                        { 'Date': {'$lte': int(End)}   },
                    ],
                    'IsOpen': 1,
                }, Sort=['Date', 1])
                return [Item['Date'] for Item in Ret]
            elif Start and Day:
                Ret = TradeDayTable.Search({
                    '$and': [
                        { 'Date': {'$gte': int(Start)} },
                    ],
                    'IsOpen': 1,
                }, Sort=['Date', 1], Limit=Day)
                return [Item['Date'] for Item in Ret]
            elif End and Day:
                Ret = TradeDayTable.Search({
                    '$and': [
                        { 'Date': {'$lte': int(End)}   },
                    ],
                    'IsOpen': 1,
                }, Sort=['Date', -1], Limit=Day)
                Ret.reverse()
                return [Item['Date'] for Item in Ret]
            elif Day:
                Ret = TradeDayTable.Search({
                    '$and': [
                        { 'Date': {'$lte': int(ChronusBear.Date().String(-1))}   },
                    ],
                    'IsOpen': 1,
                }, Sort=['Date', -1], Limit=Day)
                Ret.reverse()
                return [Item['Date'] for Item in Ret]
            else:
                raise BadBear('--------GetTradeDay Para Error---------')


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
                    return "Don't Need Update"
            else:
                return self.Update(Start=999, End=LastTradeDay)

        def Update(self, Start, End):
            if Start == 999:
                Start = '20000101'
            Tick = tushare.pro_bar(ts_code = self.TSCode, adj='qfq', start_date=str(Start), end_date=str(End))
            if len(Tick) == 0:
                return 'Stock Is Dead'

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
            return 'Success'

        def GetLatestDay(self):
            LatestDay = self.TickTable.Search({},Sort=['Date', -1],Limit=1)
            if len(LatestDay) != 0:
                return LatestDay[0]
            else:
                raise GlobalBear.BadBear('Stock Does Not Exist')

        def GetRange(self, Start, End):
            Ret = self.TickTable.Search({
                '$and': [
                    {'Date': {'$gte': Start}},
                    {'Date': {'$lte': End}}]
            })
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
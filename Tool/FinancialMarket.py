import os,sys
import tushare
import talib
import numpy
import pandas
import warnings
warnings.filterwarnings('ignore')

import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Multitask as MultitaskBear
import PyBear.Library.Statistics as StatisticsBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Chart as ChartBear
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


class Quantification:
    def Profit(Data, Days):
        return Data[-1] - Data[-1-Days]


    def MA(Data, days=120, range=5):
        return talib.MA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 

    def EMA(Data, days=120, range=5):
        return talib.EMA(numpy.array(self.stockInfo.getOpen(days=days)), timeperiod=range) 

    def BOLL(Data, days=120, range=5):
        pass

    def MACD(Data, fastperiod=12, slowperiod=26, signalperiod=9):
        DIF, DEA, MACD = talib.MACD(
        numpy.array(Data),
        fastperiod=fastperiod, 
        slowperiod=slowperiod, 
        signalperiod=signalperiod)
        return DIF, DEA, MACD*2

    def RSV(Close, High, Low):
        return talib.STOCH(
            numpy.array(High),
            numpy.array(Low),
            numpy.array(Close),
            fastk_period = 1,
            slowk_period = 1,
            slowk_matype = 0,
            slowd_period = 5,
            slowd_matype = 0,)

    def RSI(Data, days=120, range=5):
        return talib.RSI(numpy.array(self.stockInfo.getOpen(days=days)), 5)

    def GetCDLIndex(Open, High, Low, Close, Daily=True):
        Open = numpy.array(Open)
        High = numpy.array(High)
        Low = numpy.array(Low)
        Close = numpy.array(Close)
        CDLIndex = {}

        CDLIndex['2CROWS'] = talib.CDL2CROWS(Open, High, Low, Close)
        CDLIndex['3BLACKCROWS'] = talib.CDL3BLACKCROWS(Open, High, Low, Close)
        CDLIndex['3INSIDE'] = talib.CDL3INSIDE(Open, High, Low, Close)
        CDLIndex['3LINESTRIKE'] = talib.CDL3LINESTRIKE(Open, High, Low, Close)
        CDLIndex['3OUTSIDE'] = talib.CDL3OUTSIDE(Open, High, Low, Close)
        CDLIndex['3STARSINSOUTH'] = talib.CDL3STARSINSOUTH(Open, High, Low, Close)
        CDLIndex['3WHITESOLDIERS'] = talib.CDL3WHITESOLDIERS(Open, High, Low, Close)
        CDLIndex['ABANDONEDBABY'] = talib.CDLABANDONEDBABY(Open, High, Low, Close)
        CDLIndex['ADVANCEBLOCK'] = talib.CDLADVANCEBLOCK(Open, High, Low, Close)
        CDLIndex['BELTHOLD'] = talib.CDLBELTHOLD(Open, High, Low, Close)
        CDLIndex['BREAKAWAY'] = talib.CDLBREAKAWAY(Open, High, Low, Close)
        CDLIndex['CLOSINGMARUBOZU'] = talib.CDLCLOSINGMARUBOZU(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLCONCEALBABYSWALL(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLCOUNTERATTACK(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLDARKCLOUDCOVER(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLDOJI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLDOJISTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLDRAGONFLYDOJI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLENGULFING(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLEVENINGDOJISTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLEVENINGSTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLGAPSIDESIDEWHITE(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLGRAVESTONEDOJI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHAMMER(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHANGINGMAN(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHARAMI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHARAMICROSS(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHIGHWAVE(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHIKKAKE(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHIKKAKEMOD(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLHOMINGPIGEON(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLIDENTICAL3CROWS(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLINNECK(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLINVERTEDHAMMER(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLKICKING(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLKICKINGBYLENGTH(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLLADDERBOTTOM(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLLONGLEGGEDDOJI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLLONGLINE(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLMARUBOZU(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLMATCHINGLOW(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLMATHOLD(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLMORNINGDOJISTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLMORNINGSTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLONNECK(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLPIERCING(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLRICKSHAWMAN(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLRISEFALL3METHODS(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSEPARATINGLINES(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSHOOTINGSTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSHORTLINE(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSPINNINGTOP(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSTALLEDPATTERN(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLSTICKSANDWICH(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLTAKURI(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLTASUKIGAP(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLTHRUSTING(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLTRISTAR(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLUNIQUE3RIVER(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLUPSIDEGAP2CROWS(Open, High, Low, Close)
        CDLIndex['2CROWS'] = talib.CDLXSIDEGAP3METHODS(Open, High, Low, Close)

        if Daily:
            Ret = []
            for Counter in range(len(CDLIndex[0])):
                APList = []
                for Item in list(CDLIndex):
                    if Item[Counter] == 0:
                        APList.append(0)
                    else:
                        APList.append(1)
                Ret.append(APList)
            return Ret
        else:
            for Item in CDLIndex:
                for Counter in range(len(Item)):
                    if Item[Counter] == 100:
                        Item[Counter] = 1
                    elif Item[Counter] == -100:
                        Item[Counter] = 2
            return CDLIndex
                        

class Brokor:
    def __init__(self, Date, Data):
        for Item in Data:
            if len(Item) != len(Date):
                raise BadBear('Broker Data Not Synchronous')

        self.DateIndex = {}
        self.Date = Date
        self.Data = Data
        IndexNumber = 0
        for Item in Date:
            self.DateIndex[Item] = IndexNumber
            IndexNumber += 1

        MinList = []
        MaxList = []
        for Item in self.Data:
            CounterList = []
            for Counter in range(len(Item)):
                if type(Item[Counter]) != list and numpy.isnan(Item[Counter]):
                    continue
                CounterList.append(Counter)
            MinList.append(min(CounterList))
            MaxList.append(max(CounterList))

        self.Start = max(MinList)
        self.End = min(MaxList)
        if self.Start > self.End:
            raise BadBear('Broker Data Not Enough')
        self.Pointer = self.Start - 1

    def __len__(self):
        return self.End - self.Start + 1

    def __iter__(self):
        return self

    def __next__(self):
        self.Pointer += 1
        if self.Pointer > self.End:
            raise StopIteration
        Ret = [self.Pointer, self.Date[self.Pointer]]
        for Item in self.Data:
            Ret.append(Item[self.Pointer])
        return Ret

    def Inspect(self, Start=None, End=None):
        if Start and End:
            pass
        elif Start:
            pass

    def GetInfo(self, Pointer, Force = False):
        if not Force:
            if Pointer > self.End:
                raise BadBear('Brokor Pointer Exceed End')
        Ret = [Pointer, Date[Pointer]]
        for Item in self.Data:
            Ret.append(Item[Pointer])
        return Ret

class Analyst:
    def DailyUpdate(LimitPerMinute=None):
        TM = MultitaskBear.TaskMatrix(2,32, LimitPerMinute=LimitPerMinute)
        #TM = MultitaskBear.TaskMatrix(1,1, LimitPerMinute=LimitPerMinute)

        CHNStockMarket = CHN.StockMarket().Init()
        LastTradeDay = CHNStockMarket.LastTradeDay()
        RedisBear.Redis('RedisLocal').delete('A')

        StockArg = [[Item, LastTradeDay] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
        print('Ready To Launch')
        TM.ImportTask(WorkLoad.StockUpdate, StockArg)
        TM.Start()

    def UpdateCheck():
        TM = MultitaskBear.TaskMatrix(2,32)

        CHNStockMarket = CHN.StockMarket()
        Redis = RedisBear.Redis('RedisLocal')
        Redis.delete('B')

        StockArg = [[Item] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
        print('Ready To Launch')
        TM.ImportTask(WorkLoad.UpdateCheck, StockArg)
        TM.Start()

        print('----------------------------------')

        Keys = Redis.hgetall('B')
        Index = list(Keys)
        Index.sort()
        for Key in Index:
            print(Key, ': ', Keys[Key])
            
    def LogCheck(StockCode=None, Filter=None):
        if StockCode:
            pass
        redis = RedisBear.Redis('RedisLocal')
        Keys = redis.hgetall('A')
        print(len(Keys))
        for Key in Keys:
            Result = Keys[Key]
            if Filter:
                if \
                    Result != 'Success' and \
                    Result != "Don't Need Update":
                    print(Key, ':', Result)
            else:
                print(Keys, ':', Result)
    
    def StrategyMACD(End):
        TM = MultitaskBear.TaskMatrix(6,4, LimitPerMinute=LimitPerMinute)

        CHNStockMarket = CHN.StockMarket().Init()
        RedisBear.Redis('RedisLocal').delete('D')

        End = CHNStockMarket.GetTradeDay(End=End, Day=120)

        StockArg = [[Item, End[0], End[-1]] for Item in CHNStockMarket.GetStockCode(TSCode=True, Filter=['SZ', 'SH'])]
        print('Ready To Launch')
        TM.ImportTask(WorkLoad.StrategyMACD, StockArg)
        TM.Start()
        

class WorkLoad:
    def Retry(Number):
        pass

    def StockUpdate(StockCode, LastTradeDay):
        ErrorCounter = 0
        while True:
            try:
                Ret = CHN.Stock(StockCode).Sync(LastTradeDay)
                RedisBear.Redis('RedisLocal').hset('A', StockCode, str(Ret))
                break
            except Exception as e:
                ErrorCounter += 1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                RedisBear.Redis('RedisLocal').hset('A', StockCode, 'Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    print('''ERROR HAPPEND: %s''' % (StockCode))
                    RedisBear.Redis('RedisLocal').hset('A', StockCode, 'Error: ' + str(e))
                    break
        print(StockCode)
        exit()

    def UpdateCheck(StockCode):
        ErrorCounter = 0
        while True:
            try:
                RedisBear.Redis('RedisLocal').hset('B', StockCode, str(CHN.Stock(StockCode).GetLatestDay()['Date']))
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 20:
                    RedisBear.Redis('RedisLocal').hset('B', StockCode, 'Error: ' + str(e))
                    break

    def StrategyMACD(Start, End):
        ErrorCounter = 0
        while True:
            try:
                Price = CHN.Stock(StockCode).GetRange(Start, End)
                break
            except Exception as e:
                ErrorCounter +=1
                print(StockCode, ': Error(' + str(ErrorCounter) +')')
                if ErrorCounter >= 10:
                    RedisBear.Redis('RedisLocal').hset('D', StockCode, 'Error: ' + str(e))
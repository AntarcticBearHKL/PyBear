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

        def UpdateStockBasicInfo(self):
            StockBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'StockBasicInfo')
            UpdateTime = StockBasicInfoTable.Search({
                'SearchID': 1
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                print('UpdateStockBasicInfo Finish(N)')
                return


            print('UpdateStockBasicInfo Start')
            BasicInfo = self.API.stock_basic()

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
                'SearchID': 1
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
            print('UpdateStockBasicInfo Finish')

        def UpdateTradeDay(self):
            TradeDayTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'TradeDay')
            UpdateTime = TradeDayTable.Search({
                'SearchID': 1
            })
            if len(UpdateTime) !=0 and (ChronusBear.Date() // ChronusBear.Date(UpdateTime[0]['UpdateTime']))[2] < 10:
                print('UpdateTradeDay Finish(N)')
                return

            print('UpdateTradeDay Start')
            EndDate = ChronusBear.Date()
            EndDate.SetTime(Month=12, Day=999)
            TradeDay = self.API.trade_cal(exchange='', start_date='20000101', end_date=EndDate.String(-1))

            Data = [{
                'UpdateTime': ChronusBear.Date().String(0),
                'SearchID': 1
            }]
            for Item in TradeDay.itertuples():
                Data.append({
                    'Date': int(Item.cal_date),
                    'IsOpen': int(Item.is_open),
                })

            
            TradeDayTable.Delete({})
            TradeDayTable.Insert(Data)
            print('UpdateTradeDay Finish')


        def GetStockCode(self, TSCode=None, Filter=[]):
            StockBasicInfoTable = MongoDBBear.MongoDB('MongoDB', 'StockCHN', 'StockBasicInfo')
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
            Ret = StockBasicInfoTable.Search({
                '$and': [
                    {'Code': {'$exists': 'true'}},
                    {'$or': Condition}
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
                TargetDay = ChronusBear.Date().ResetTime(Day=-1).String(-1)
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
            pass

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
        def __init__(self, ServerName, UserName, Code):
            if TushareAvailiable:
                raise BadBear('Tushare Cannot Use Without Token')
            self.ServerName = ServerName
            self.UserName = UserName
            self.Code = Code
            self.StockMarket = None
             
            self.TickTable = MySQLTable(ServerName, UserName, 'CHNStockMarket', self.Code[:6]+'_Price')


        def Sync(self, LastTradeDay):
            if self.NeedFullDownload():
                print(self.Code+' Sync Full Download')
                self.FullDownload() 
                return

            (UpdateCheck, Start, End) = self.NeedUpdate(LastTradeDay)
            if UpdateCheck:
                print(self.Code+' Sync Update')
                self.Update(Start, End)

            print(self.Code+' Synchronize Finished')

        def FullDownload(self):
            print(self.Code+' Full Download Start')
            self.TickTable.InitTable({
                'Date':             'INT NOT NULL DEFAULT 0',
                'Open':             'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'High':             'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Low':              'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Close':            'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'ChangedPrice':     'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'ChangedPercent':   'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Volume':           'DECIMAL(13,4) NOT NULL DEFAULT 0',
                'Amount':           'DECIMAL(13,4) NOT NULL DEFAULT 0',
            }, Index=['Date'])

            Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date='20050101', end_date=Date().String(Style='SS'))

            if Tick:
                Tick = Tick.dropna()
            else:
                print(self.Code+' Full Download Finished')
                return

            Values = []
            for Item in Tick.itertuples():
                Values.append([
                    int(Item.trade_date),
                    round(float(Item.open), 6),
                    round(float(Item.high), 6),
                    round(float(Item.low), 6),
                    round(float(Item.close), 6),
                    round(float(Item.change), 6),
                    round(float(Item.pct_chg), 6),
                    round(float(Item.vol), 6),
                    round(float(Item.amount), 6),
                    ])
            Values.reverse()

            self.TickTable.DeleteAll()
            self.TickTable.Insert(['Date', 'Open', 'High', 'Low', 'Close', 'ChangedPrice', 'ChangedPercent', 'Volume', 'Amount'], Values)

            print(self.Code+' Full Download Finished')

        def Update(self, Start, End):
            Tick = tushare.pro_bar(ts_code = self.Code, adj='qfq', start_date=Start, end_date=End)

            Values = []
            for Item in Tick.itertuples():
                Values.append([
                    int(Item.trade_date),
                    round(float(Item.open), 6),
                    round(float(Item.high), 6),
                    round(float(Item.low), 6),
                    round(float(Item.close), 6),
                    round(float(Item.change), 6),
                    round(float(Item.pct_chg), 6),
                    round(float(Item.vol), 6),
                    round(float(Item.amount), 6),
                    ])
            Values.reverse()

            self.TickTable.Insert(['Date', 'Open', 'High', 'Low', 'Close', 'ChangedPrice', 'ChangedPercent', 'Volume', 'Amount'], Values)

        def NeedFullDownload(self):
            if not self.TickTable.GetRowNumber():
                return True
            return False

        def NeedUpdate(self, LastTradeDay):
            CurrentTradeDay = self.TickTable.SearchTable(Column='MAX(Date)')[0][0]

            if int(CurrentTradeDay) < int(LastTradeDay):
                RequestStart = Date(CurrentTradeDay).ResetTime(Day=1).String(Style=Style_SS)
                return True, str(RequestStart), str(LastTradeDay)
            return False, '', ''

        def IsAvailable(self, LastTradeDay):
            if Stock.NeedFullDownload() or Stock.NeedUpdate(LastTradeDay)[0]:
                return False
            return True


        def GetData(self, Start, End, DataName):
            Result = self.TickTable.SearchTable(Column=DataName, Condition='''WHERE Date>=%s AND Date<=%s'''%(Start, End))
            Ret = []
            for Item in Result:
                Ilist = []
                for Itemm in Item:
                    Ilist.append(float(Itemm))
                Ret.append(Ilist)
            return Ret

        def PlotData(self, Start, End):
            DateList = [str(int(Item[0])) for Item in self.GetData(Start, End, 'Date')]
            PriceList = self.GetData(Start, End, 'Open, Close, Low, High')
            
            return GetKLine([
                DateList,
                {'Price':PriceList}
            ])
            

        def GetTableSize(self):
            return self.TickTable.GetTableSize()

        def GetRowNumber(self):
            return self.TickTable.GetRowNumber()
              
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
        TM = TaskMatrix(2,16, LimitPerMinute=LimitPerMinute)
        #TM = TaskMatrix(1,1, LimitPerMinute=LimitPerMinute)

        CHNStockMarket = CHN.StockMarket(ServerName, UserName)
        if Init:       
            CHNStockMarket.UpdateBasicInfo()
            CHNStockMarket.UpdateTradeDay()
            CHNStockMarket.CheckStockTable()

        LTD = CHNStockMarket.LastTradeDay()

        CacheList = TM.GetCacheList()

        StockArg = [[ServerName, UserName, Item, LTD, CacheList] for Item in CHNStockMarket.AllStock()]

        print('Ready To Launch')

        TM.ImportTask(WorkLoad.StockUpdate, StockArg)
        TM.Start()

        print(CacheList)

    def NeedUpdate(ServerName, UserName):
        TM = TaskMatrix(2,16)
        CHNStockMarket = CHN.StockMarket(ServerName, UserName)

        LTD = CHNStockMarket.LastTradeDay()

        CacheList = TM.GetCacheList()

        StockArg = [[ServerName, UserName, Item, LTD, CacheList] for Item in CHNStockMarket.AllStock()]
        print('Ready To Launch')

        TM.ImportTask(WorkLoad.NeedUpdate, StockArg)
        TM.Start()

        print(CacheList)
            

class WorkLoad:
    def StockUpdate(ServerName, UserName, StockCode, LastTradeDay, CacheList):
        ErrorCounter = 0
        while True:
            try:
                CHN.Stock(ServerName, UserName, StockCode).Sync(LastTradeDay)
                break
            except Exception as e:
                ErrorCounter += 1
                if ErrorCounter >= 10:
                    print(e)
                    print('''ERROR HAPPEND: %s''' % (StockCode))
                    CacheList.append(StockCode)
                    break

    def NeedUpdate(ServerName, UserName, StockCode, LastTradeDay, CacheList):
        ErrorCounter = 0
        while True:
            try:
                print(StockCode)
                Stock = CHN.Stock(ServerName, UserName, StockCode)
                if Stock.NeedFullDownload() or Stock.NeedUpdate(LastTradeDay)[0]:
                    CacheList.append(StockCode)
                break
            except Exception as e:
                ErrorCounter += 1
                if ErrorCounter >= 10:
                    print(e)
                    print('''ERROR HAPPEND: %s''' % (StockCode))
                    CacheList.append('ERROR: ' + StockCode)
                    break
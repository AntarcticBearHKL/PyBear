import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.Redis as RedisBear

class Config:
    def __init__(self, LogName=None, StockCode=None, Filter=None, nFilter=None):
        self.LogName = LogName
        self.StockCode = StockCode
        self.Filter = Filter
        self.nFilter = nFilter

    def Run(self):
        Database = RedisBear.Redis('RedisLocal')
        if self.LogName == None:
            print(Database.keys())
            return
        Keys = Database.hgetall(self.LogName)
        Index = list(Keys)
        Index.sort()

        for Key in Index:
            Result = Keys[Key]
            if self.Filter:
                if Result in Filter:
                    print(Key, ':', Result)
            elif self.nFilter:
                if Result not in Filter:
                    print(Key, ':', Result)
            elif self.StockCode:
                if Key in StockCode:
                    print(Key, ':', Result)
            else:
                print(Key, ':', Result)
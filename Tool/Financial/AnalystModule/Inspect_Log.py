

def LogCheck(LogName, StockCode=None, Filter=None, nFilter=None):
        redis = RedisBear.Redis('RedisLocal')
        Keys = redis.hgetall(LogName)
        Index = list(Keys)
        Index.sort()

        for Key in Index:
            Result = Keys[Key]
            if Filter:
                if Result in Filter:
                    print(Key, ':', Result)
            elif nFilter:
                if Result not in Filter:
                    print(Key, ':', Result)
            elif StockCode:
                if Key in StockCode:
                    print(Key, ':', Result)
            else:
                print(Key, ':', Result)


def UpdateCheck():
    TM = MultitaskBear.TaskMatrix(2,32)

    CHNStockMarket = CHN.StockMarket()
    Redis = RedisBear.Redis('RedisLocal')
    Redis.delete('UpdateCheck')

    StockArg = [[Item] for Item in CHNStockMarket.GetStockCode(TSCode=True)]
    print('Ready To Launch')
    TM.ImportTask(WorkLoad.UpdateCheck, StockArg)
    TM.Start()

    print('----------------------------------')
    Analyst.LogCheck('UpdateCheck')

def UpdateCheck(StockCode):
    ErrorCounter = 0
    while True:
        try:
            RedisBear.Redis('RedisLocal').hset('UpdateCheck', StockCode, str(CHN.Stock(StockCode).GetLatestDay()['Date']))
            break
        except Exception as e:
            ErrorCounter +=1
            print(StockCode, ': Error(' + str(ErrorCounter) +')')
            if ErrorCounter >= Number:
                RedisBear.Redis('RedisLocal').hset('UpdateCheck', StockCode, 'Error: ' + str(e))
                break
    
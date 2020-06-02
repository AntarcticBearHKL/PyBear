import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Tool.Authentication as Authentication
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear

def NewEvent(MongoServerName, RedisServerName, Username, Date, Label, Info, Append, CustomDate = None): 
    Table = MongoDBBear.MongoDBTable(
        MongoServerName,
        GlobalBear.TimeCapsuleDatabaseName, 
        Username)
    Table.Insert({
        'Date': Date.TimestampR(),
        'UnionID': CipherBear.NumberIndex(),
        'Label': Label,
        'Info': Info,
        'Append': Append,
    })

def NewPeriod(ServerName, AuthenticationCode, Period, Label, Info, Append):
    pass

def GetPeriod(MongoServerName, RedisServerName, AuthenticationCode, Period, Label):
    Result = Authentication.UserAuthentication(RedisServerName, AuthenticationCode)
    if Result[0] != 'TimeCapsule':
        return 'Authentication Failed'
    Table = MongoDBBear.MongoDBTable(
        MongoServerName,
        GlobalBear.TimeCapsuleDatabaseName, 
        Result[1])
    Condition = {
        'Label': Label,
        '$and': [
            {'Date': {'$gte' : Period[0].Timestamp()}},
            {'Date': {'$lte' : Period[1].Timestamp()}},
        ]
    }
    Ret = Table.Search(Condition)
    return Ret

def GetDay(ServerName, AuthenticationCode, Day):
    pass
import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Tool.Authentication as Authentication
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear

def NewEvent(ServerName, AuthenticationCode, Label, Info, Append):
    Table = MongoDBBear.MongoDBTable(
        ServerName,
        GlobalBear.AuthenticationDatabaseName, 
        ServiceName)
    Table.Insert({
        'Date': ChronusBear.Date().Timestamp(),
        'UnionID': CipherBear.NumberIndex(),
        'Label': Label,
        'Info': Info,
        'Append': Append,
    })

def NewPeriod(ServerName, AuthenticationCode, Period, Label, Info, Append):
    pass

def GetPeriod(ServerName, AuthenticationCode, Period, Label):
    pass

def GetDay(ServerName, AuthenticationCode, Day):
    pass
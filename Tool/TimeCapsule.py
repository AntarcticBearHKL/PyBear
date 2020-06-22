import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Tool.Authentication as Authentication
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear

def NewEvent(Username, Label, Date, Content, Common, SubLabel): 
    Table = MongoDBBear.MongoDB(
        'MongoDB',
        GlobalBear.TimeCapsuleDatabaseName, 
        Username)
    Table.Insert({
        'Label': Label,
        'UnionID': CipherBear.NumberIndex(),
        'Date': str(Date),
        'Content': Content,
        'Common': Common,
        'SubLabel': SubLabel,
    })

def NewPeriod(ServerName, Period, Label, Info, Append):
    pass

def GetPeriod(Username, Period, Label):
    Table = MongoDBBear.MongoDB(
        'MongoDB',
        GlobalBear.TimeCapsuleDatabaseName, 
        Username)
    Condition = {
        'Label': Label,
        '$and': [
            {'Date': {'$gte' : Period[0]}},
            {'Date': {'$lte' : Period[1]}},
        ]
    }
    return Table.Search(Condition)

def GetDay(Date):
    Table = MongoDBBear.MongoDB(
        'MongoDB',
        GlobalBear.TimeCapsuleDatabaseName, 
        Username)
    Condition = {
        'Date': Date,
    }
    return Table.Search(Condition)
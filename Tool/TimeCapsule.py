import json

import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MongoDB as MongoDBBear
import PyBear.Library.Data.MySQL as MySQLBear
import PyBear.Library.Chronus as ChronusBear
import PyBear.Library.Cipher as CipherBear

class DairyBook:
    def __init__(self, Username, DairyBookName):
        self.Table = MongoDBBear.MongoDB(
            'MongoDB',
            GlobalBear.TimeCapsuleDatabaseName, 
            Username)
        self.DairyBookName = DairyBookName

    def NewEvent(self, Content, Additional=None): 
        if Additional:
            Additional = json.loads(Additional)
        else:
            Additional = {}
        self.Table.Insert({
            'ServiceID': 1,
            'UnionID': CipherBear.NumberIndex(),
            'CreateDate': ChronusBear.Date().String(0),
            'Content': Content,
            'Additional': Additional,
        })

    def GetPeriod(self, Period):
        self.Table = MongoDBBear.MongoDB(
            'MongoDB',
            GlobalBear.TimeCapsuleDatabaseName, 
            Username)
        Condition = {
            '$and': [
                {'Date': {'$gte' : Period[0]}},
                {'Date': {'$lte' : Period[1]}},
            ]
        }
        return Table.Search(Condition)

    def GetDay(self, Date):
        self.Table = MongoDBBear.MongoDB(
            'MongoDB',
            GlobalBear.TimeCapsuleDatabaseName, 
            Username)
        Condition = {
            'Date': Date,
        }
        return Table.Search(Condition)

class NoteBook:
    def __init__(self):
        pass

class Contact:
    def __init__(self):
        pass

class Balance:
    def __init__(self):
        pass

class File:
    def __init__(self):
        pass
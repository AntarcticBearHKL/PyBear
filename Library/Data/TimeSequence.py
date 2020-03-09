import json

from PyBear.GlobalBear import *
from PyBear.Library.Data.MySQL import *
from PyBear.Library.Chronus import *

class TimeSequence:
    def __init__(self, TimeSequenceName, Username, Password, Ip='127.0.0.1', Port=3306):
        self.TableName = TimeSequenceName
        NewDatabasesServer(TimeSequenceName+'_DatabaseServer', Username, Password, Ip=Ip, Port=Port)
        self.Databases = Database(TimeSequenceName+'_DatabaseServer', TimeSequenceName)

    def getStartDate(self):
        if len(self.Lines) == 0:
            return None
        else:
            return list(self.Lines).sort()[0]

    def getEndDate(self):
        if len(self.Lines) == 0:
            return None
        else:
            return list(self.Lines).sort()[-1]

    def __getitem__(self, item):
        if type(item) == str:
            if item in self.Lines:
                return self.Lines[item]
            else:
                print('get item error')
        if type(item) == list:
            ret = []
            for date in item:
                ret.append(self.Lines[date])
            return ret

    def __setitem__(self, Time, Value):
        self.Databases.Insert(self.TableName, {
            'Date': Time,
            'TimeStamp': Date(Time),
            'Value': Value
        })

if GlobalAvailabilityCheck:
    pass
import json

from BearPY.GlobalBear import *
from BearPY.Libraries.RegularExpression import *
from BearPY.Libraries.Data.MySQL import *
from BearPY.Libraries.Time import *

class TimeSequence:
    def __init__(self, TimeSequenceName, Username, Password, Ip='127.0.0.1', Port=3306):
        NewDatabasesServer(TimeSequenceName+'_DatabaseServer', Username, Password, Ip=Ip, Port=Port)
        self.Databases = Database(TimeSequenceName+'_DatabaseServer', TimeSequenceName)
        
    def Feed(self, ValueDict):
        for date in valueDict:
            self.Lines[date] = valueDict[date]
        self.save()

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

    def __setitem__(self, item, value):
        self.Lines[item] = value
        self.save()

if GlobalAvailabilityCheck:
    pass
import PyBear.GlobalBear as GlobalBear
import pymongo

 #db.createUser({'user':'Debuger', 'pwd':'A11b22;;', 'roles':[{'role':'readWrite', 'db':'Authentication'}], 'mechanisms':['SCRAM-SHA-1']]});

class MongoDB:
    def __init__(self, ServerName, UserName, DatabasesName):
        self.ServerName = ServerName
        self.UserName = UserName
        self.DatabasesName = DatabasesName
        self.Connection = pymongo.MongoClient(
            host = GlobalBear.GetServer(ServerName).IP, 
            port = GlobalBear.GetServer(ServerName).Port)
        self.Connection[DatabasesName].authenticate(
            GlobalBear.GetUser(UserName).UserName, 
            GlobalBear.GetUser(UserName).Password, 
            mechanism='SCRAM-SHA-1')

        self.Database = self.Connection[self.DatabasesName]

    def ListTable(self):
        return self.Database.list_collection_names()

    def DeleteTable(self, TableName):
        self.Database[TableName].drop()

class MongoDBTable:
    def __init__(self, ServerName, UserName, DatabasesName, TableName):
        self.ServerName = ServerName
        self.UserName = UserName
        self.DatabasesName = DatabasesName
        self.TableName = TableName

        self.Connection = pymongo.MongoClient(
            host = GlobalBear.GetServer(ServerName).IP, 
            port = GlobalBear.GetServer(ServerName).Port)
        self.Connection[DatabasesName].authenticate(
            GlobalBear.GetUser(UserName).UserName, 
            GlobalBear.GetUser(UserName).Password, 
            mechanism='SCRAM-SHA-1')
        
        self.Table = self.Connection[self.DatabasesName][self.TableName]

    def Insert(self, Data):
        if type(Data) == dict:
            self.Table.insert_one(Data)
        elif type(Data) == list:
            self.Table.insert_many(Data)

    def Change(self, Condition, Value):
        Ret = self.Table.update_many(Condition, Value)
        return (Ret.matched_count, Ret.modified_count)

    def Search(self, Condition, Count=None, Sort=None, Limit=None):
        if Count:
            Ret = self.Table.find(Condition).count()
        elif Sort and not Limit:
            Ret = self.Table.find(Condition).sort(Sort[0], Sort[1])
        elif Sort and Limit:
            Ret = self.Table.find(Condition).sort(Sort[0], Sort[1]).limit(Limit)
        elif Limit:
            Ret = self.Table.find(Condition).limit(Limit)
        else:
            Ret = self.Table.find(Condition)

        return [Item for Item in Ret]

    def Delete(self, Condition):
        return self.Table.delete_many(Condition).deleted_count
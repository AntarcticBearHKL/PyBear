from PyBear.GlobalBear import *
import pymongo

class MongoDB:
    def __init__(self, ServerName, UserName, DatabasesName):
        self.ServerName = ServerName
        self.UserName = UserName
        self.DatabasesName = DatabasesName
        self.Connection = pymongo.MongoClient(
            '''mongodb://%s:%s@%s:%s/'''%(
            GetUser(UserName).UserName, 
            GetUser(UserName).Password, 
            GetServer(ServerName).IP, 
            GetServer(ServerName).Port))

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
            '''mongodb://%s:%s@%s:%s/'''%(
            GetUser(UserName).UserName, 
            GetUser(UserName).Password, 
            GetServer(ServerName).IP, 
            GetServer(ServerName).Port))
        
        self.Table = self.Connection[self.DatabasesName][self.TableName]

    def Insert(self, Data):
        self.Table.insert_many(Data)

    def Change(self, Condition, Value):
        Ret = self.Table.update_many(Condition, Value)
        return (Ret.matched_count, Ret.modified_count)

    def Search(self, Condition, Count=None, Sort=None, Limit=None):
        if Count:
            self.Table.find(Condition).count()
        elif Sort and not Limit:
            self.Table.find(Condition).sort(Sort[0], Sort[1])
        elif Sort and Limit:
            self.Table.find(Condition).sort(Sort[0], Sort[1]).limit(Limit)
        elif Limit:
            self.Table.find(Condition).limit(Limit)
        else:
            self.Table.find(Condition)

    def Delete(self, Condition):
        return self.Table.delete_many(Condition).deleted_count
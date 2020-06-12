import PyBear.GlobalBear as GlobalBear
import pymongo

#db.createUser({'user':'Debuger', 'pwd':'A11b22;;', 'roles':[{'role':'readWrite', 'db':'StockCHN'}], 'mechanisms':['SCRAM-SHA-1']});

class MongoDB:
    def __init__(self, ServerName, DatabasesName, TableName=None):
        self.ServerName = ServerName
        self.DatabasesName = DatabasesName
        self.TableName = TableName

        self.Connection = pymongo.MongoClient(
            host = GlobalBear.Server(ServerName).IP, 
            port = GlobalBear.Server(ServerName).Port)
        self.Connection[DatabasesName].authenticate(
            GlobalBear.Server(ServerName).Username, 
            GlobalBear.Server(ServerName).Password, 
            mechanism='SCRAM-SHA-1')
        

    def SetTable(self, TableName):
        self.TableName = TableName


    def ListTable(self):
        return self.Connection[self.DatabasesName].list_collection_names()

    def DeleteTable(self, TableName):
        self.Connection[self.DatabasesName][TableName].drop()



    def Insert(self, Data):
        if not self.TableName:
            raise GlobalBear.BadBear('')
        self.Table = self.Connection[self.DatabasesName][self.TableName]

        if type(Data) == dict:
            self.Table.insert_one(Data)
        elif type(Data) == list:
            self.Table.insert_many(Data)

    def Change(self, Condition, Value):
        if not self.TableName:
            raise GlobalBear.BadBear('')
        self.Table = self.Connection[self.DatabasesName][self.TableName]

        Ret = self.Table.update_many(Condition, Value)
        return (Ret.matched_count, Ret.modified_count)

    def Search(self, Condition, Count=None, Sort=None, Limit=None):
        if not self.TableName:
            raise GlobalBear.BadBear('')
        self.Table = self.Connection[self.DatabasesName][self.TableName]

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
        if not self.TableName:
            raise GlobalBear.BadBear('')
        self.Table = self.Connection[self.DatabasesName][self.TableName]
            
        return self.Table.delete_many(Condition).deleted_count

if GlobalBear.GlobalTestModuleOn:
    TestDB = MongoDB('MongoDB', 'Test', 'MongoDB_Test')
    TestDB.Delete({})
    TestDB.Insert({
        'Test' : 'Success'
    })
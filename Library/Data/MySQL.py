import pymysql
import os, sys

from PyBear.GlobalBear import *
from PyBear.Library.Chronus import *

class Database:
    def __init__(self, ServerName, UserName, DatabaseName):
        self.Connection = pymysql.connect(
            host=GetServer(ServerName).IP,
            port=GetServer(ServerName).Port,
            user=GetUser(UserName).UserName,
            passwd=GetUser(UserName).Password,
            db=DatabaseName,)
        self.ServerName = ServerName
        self.UserName = UserName
        self.DatabaseName = DatabaseName
        self.Cursor = self.Connection.cursor()
    
    def __ShowResult(self):
        return self.Cursor.fetchall()

    def __Commit(self):
        self.Connection.commit()

    def __Execute(self, SQL):
        self.Cursor.execute(SQL)
        self.__Commit()
        return self.__ShowResult()


    def Table(self, TableName):
        return DatabaseTable(self.ServerName, self.UserName, self.DatabaseName, TableName)

    def ListTables(self):
        return [Item[0] for Item in self.__Execute('''SHOW TABLES;''')]

    def CheckTable(self, TableList):
        ServerTableList = self.ListTables()
        for Item in TableList:
            if Item not in ServerTableList:
                SQL = '''CREATE TABLE %s (ID INT AUTO_INCREMENT, PRIMARY KEY(ID)) CHARSET=utf8;''' % (Item)
                self.__Execute(SQL)
    
    def DeleteTables(self, Condition):
        SQL = '''select concat('drop table ', table_name, ';') from information_schema.tables where table_name like '%s';''' % (Condition)
        for SQL in self.__Execute(SQL):
            print(SQL)
            self.__Execute(SQL[0])


class DatabaseTable:
    def __init__(self, Database, TableName):
        self.DatabaseName = DatabaseName
        self.TableName = TableName

        self.Connection = pymysql.connect(
            host=GetServer(ServerName).IP,
            port=GetServer(ServerName).Port,
            user=GetUser(UserName).UserName,
            passwd=GetUser(UserName).Password,
            db=DatabaseName,)
        self.Cursor = self.Connection.cursor()
    
    def __ShowResult(self):
        return self.Cursor.fetchall()

    def __Commit(self):
        self.Connection.commit()

    def __Execute(self, SQL):
        self.Cursor.execute(SQL)
        self.__Commit()
        return self.__ShowResult()


    def NewColumn(self, ColumnName, DataType):
        SQL = '''ALTER TABLE %s ADD %s %s;''' % (self.TableName, ColumnName, DataType)
        self.__Execute(SQL)
        self.Columns = self.ListColumn()

    def ChangeColumn(self, ColumnName, DataType):
        SQL = '''ALTER TABLE %s MODIFY %s %s;''' % (self.TableName, ColumnName, DataType)
        self.__Execute(SQL)
        self.Columns = self.ListColumn()

    def DeleteColumn(self, ColumnName):
        SQL = '''ALTER TABLE %s DROP %s %s;''' % (self.TableName, ColumnName)
        self.__Execute(SQL)
        self.Columns = self.ListColumn()

    def ListColumn(self):
        SQL = '''SHOW COLUMNS FROM %s''' % (self.TableName)
        Ret = {}
        for Item in self.__Execute(SQL):
            Ret[Item[0]] = Item[1].upper()
        return Ret

    def CheckColumn(self, Columns, Index=None, UniqueIndex=None, FulltextIndex=None):
        self.Columns = self.ListColumn()
        self.Indexs = self.ListIndex()

        for Item in Columns:
            if Item in self.Columns:
                if Columns[Item].split(' ')[0] != self.Columns[Item]:
                    self.ChangeColumn(Item, Columns[Item])
            else:
                self.NewColumn(Item, Columns[Item])

        if type(Index) == list:
            for Item in Index:
                self.NewIndex(Item)
        elif type(Index) == dict:
            for Item in Index:
                self.NewIndex(Index[Item], Item)
        
        if type(UniqueIndex) == list:
            pass
        elif type(UniqueIndex) == dict:
            pass
        
        if type(FulltextIndex) == list:
            pass
        elif type(FulltextIndex) == dict:
            pass


    def NewIndex(self, ColumnName, IndexName=None):
        Indexs = [item[2] for item in self.__Execute('''SHOW KEYS FROM %s''' % (self.TableName))]

        if type(ColumnName) == list:
            if (IndexName) and (IndexName not in Indexs):
                ColumnName = ','.join(ColumnName)
                SQL = '''ALTER TABLE %s ADD INDEX %s(%s)''' % (self.TableName, IndexName, ColumnName)
            else:
                return
        elif type(ColumnName) == str:
            if ColumnName+'_INDEX' not in Indexs:
                SQL = '''ALTER TABLE %s ADD INDEX %s(%s)''' % (self.TableName, ColumnName+'_INDEX', ColumnName)
            else:
                return
        self.__Execute(SQL)
        self.Indexs = self.ListIndex()

    def NewUniqueIndex(self):
        pass

    def NewFulltextIndex(self):
        pass

    def DeleteIndex(self):
        SQL = '''DROP INDEX %s ON %s ; %s''' % (IndexName, self.TableName)
        self.__Execute(SQL)
    
    def ListIndex(self):
        SQL = '''SHOW KEYS FROM %s''' % (self.TableName)
        Ret = {}
        for Item in self.__Execute(SQL):
            if Item[2] not in Ret:
                Ret[Item[2]] = {Item[4]:Item[3]}
            else:
                Ret[Item[2]][Item[4]] = Item[3]
        return Ret


    def Insert(self, ColumnName, Data):    
        ColumnName = ','.join(ColumnName)

        for Item in Data:
            ValueInserted = ''
            for Member in Item:
                if type(Member) == str:
                    ValueInserted += '\'' + Member + '\','
                elif type(Member) == int or type(Member) == float:
                    ValueInserted += str(Member) + ','
                elif type(Member) == list:
                    ValueInserted += str(Member[0]) + ','
            ValueInserted = ValueInserted[:-1]
            SQL = '''INSERT INTO %s (%s) VALUES (%s);''' % (self.TableName, ColumnName, ValueInserted)
            self.Cursor.execute(SQL) 
        self.__Commit()
    
    def Delete(self, ID):
        if type(ID) == list:
            for Item in ID:
                self.Cursor.execute('''DELETE FROM %s WHERE ID = %s;''' % (self.TableName, Item))
        else:
            self.Cursor.execute('''DELETE FROM %s WHERE ID = %s;''' % (self.TableName, ID))
        self.__Commit()
    
    def DeleteAll(self):
        self.Cursor.execute('''TRUNCATE TABLE %s;''' % (self.TableName))

    def Change(self, ID, ColumnName, Value):
        SQL = '''UPDATE %s SET %s = %s WHERE ID = %s;''' % (self.TableName, ColumnName, Value, ID)
        print(SQL)
        self.__Execute(SQL)


    def SearchTable(self, Column='*', Condition=''):
        return self.__Execute('''SELECT %s FROM %s %s''' % (Column, self.TableName, Condition))


    def Distinct(self, ColumnName):
        SQL = '''DELETE %s FROM %s, (SELECT min(id) AS mid, %s FROM %s GROUP BY %s) AS t2 WHERE %s.id != t2.mid;''' % (self.TableName, self.TableName, ColumnName, self.TableName, ColumnName, self.TableName)
        self.__Execute(SQL)

    def GetTableSize(self):
        SQL = ''' SELECT DATA_LENGTH as data from information_schema.TABLES where table_schema='%s' and table_name='%s'; ''' % (self.DatabaseName, self.TableName)
        return self.__Execute(SQL)[0][0]

    def GetRowNumber(self):
        SQL = '''SELECT COUNT(*) FROM %s;''' % (self.TableName)
        return self.__Execute(SQL)[0][0]


class UpdateManager:
    def __init__(self, DatabaseTable):
        self.DatabaseTable = DatabaseTable
        self.DatabaseTable.CheckColumn({
            'ItemIDX': 'BIGINT NOT NULL',
            'ItemName': 'CHAR(64) NOT NULL',
            'UpdateTime': 'CHAR(16) NOT NULL',
        }, Index={'ItemIndex':['ItemIDX', 'ItemName']})

    def Update(self, Name):
        Recode = self.DatabaseTable.SearchTable(Column='ID', Condition='''WHERE ItemIDX=CRC32('%s') AND ItemName='%s' ''' % (Name, Name))
        if len(Recode) == 1: 
            self.DatabaseTable.Change(Recode[0], 'UpdateTime', Date().String())
        elif len(Recode) == 0:
            self.DatabaseTable.Insert( 
            ['ItemIDX', 'ItemName', 'UpdateTime'], 
            [[
                ['''CRC32('%s')''' % (Name)], 
                Name, 
                Date().String(),
            ],])
        print('''Update %s At %s''' % (Name, Date().String(Style=Style_L)))

    def TableUpdateTime(self, Name):
        Result = self.DatabaseTable.SearchTable(Condition='''WHERE ItemIDX=CRC32('%s') AND ItemName='%s' ''' % (Name, Name))
        if len(Result) == 0:
            return None
        else:
            return Date(Result[0][3])
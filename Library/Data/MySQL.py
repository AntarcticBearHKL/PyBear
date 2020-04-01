import pymysql
import os, sys

from PyBear.GlobalBear import *
from PyBear.Library.Chronus import *

class DatabaseTable():
    def __init__(self, ServerName, UserName, DatabaseName, TableName, Reload = False):
        self.Connection = pymysql.connect(
            host=GetServer(ServerName).IP,
            port=GetServer(ServerName).Port,
            user=GetUser(UserName).UserName,
            passwd=GetUser(UserName).Password,
            db=DatabaseName,)
        self.DatabaseName = DatabaseName
        self.TableName = TableName
        self.Cursor = self.Connection.cursor()

        Tables = [Item[0] for Item in self.__Execute('''SHOW TABLES;''')]
        if self.TableName not in Tables:
            SQL = '''CREATE TABLE %s (ID INT AUTO_INCREMENT, PRIMARY KEY(ID)) CHARSET=utf8;''' % (self.TableName)
            self.__Execute(SQL)
        elif Reload:
            self.__Execute('''DROP TABLE %s''' % (self.TableName))
            SQL = '''CREATE TABLE %s (ID INT AUTO_INCREMENT, PRIMARY KEY(ID)) CHARSET=utf8;''' % (self.TableName)
            self.__Execute(SQL)

        self.ListColumns()
    
    def __ShowResult(self):
        return self.Cursor.fetchall()

    def __Commit(self):
        self.Connection.commit()

    def __Execute(self, SQL):
        self.Cursor.execute(SQL)
        self.__Commit()
        return self.__ShowResult()



    def AddColumn(self, ColumnName, DataType):
        if ColumnName in self.Columns:
            return

        SQL = '''ALTER TABLE %s ADD %s %s;''' % (self.TableName, ColumnName, DataType)
        self.__Execute(SQL)

    def AddIndex(self, ColumnName, IndexName=None):
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
        self.ListColumns()

    def AddUniqueIndex(self):
        pass

    def AddFulltextIndex(self):
        pass

    def ListColumn(self, ColumnName):
        SQL = '''SELECT %s FROM %s''' % (ColumnName, self.TableName)
        return self.__Execute(SQL)

    def ListColumns(self):
        SQL = '''SHOW COLUMNS FROM %s''' % (self.TableName)
        self.ColumnsDetail = self.__Execute(SQL)
        self.Columns = [Item[0] for Item in self.ColumnsDetail]
        return self.ColumnsDetail

    def CheckColumn(self, Columns, Index=None, UniqueIndex=None, FulltextIndex=None):
        for Item in Columns:
            self.AddColumn(Item, Columns[Item])

        if type(Index) == list:
            for Item in Index:
                self.AddIndex(Item)
        elif type(Index) == dict:
            for Item in Index:
                self.AddIndex(Index[Item], Item)
        
        if type(UniqueIndex) == list:
            pass
        elif type(UniqueIndex) == dict:
            pass
        
        if type(FulltextIndex) == list:
            pass
        elif type(FulltextIndex) == dict:
            pass

    def ListIndex(self):
        SQL = '''SHOW KEYS FROM %s''' % (self.TableName)
        return self.__Execute(SQL)



    def Insert(self, ColumnName, Data):
        for Item in ColumnName:
            if Item not in self.Columns:
                return        
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
        if ColumnName not in self.Columns:
            return

        SQL = '''UPDATE %s SET %s = %s WHERE ID = %s;''' % (self.TableName, ColumnName, Value, ID)
        self.__Execute(SQL)



    def ListTable(self): 
        return self.__Execute('''SELECT * FROM %s''' % (self.TableName))

    def SearchTable(self, Condition, Columns='*'):
        return self.__Execute('''SELECT %s FROM %s %s''' % (Columns, self.TableName, Condition))

    def SearchID(self, Condition):
        return [Item[0] for Item in self.SearchTable(Condition)]


    def Distinct(self, ColumnName):
        SQL = '''DELETE %s FROM %s, (SELECT min(id) AS mid, %s FROM %s GROUP BY %s) AS t2 WHERE %s.id != t2.mid;''' % (self.TableName, self.TableName, ColumnName, self.TableName, ColumnName, self.TableName)
        self.__Execute(SQL)

    def TableSize(self):
        SQL = ''' SELECT CONCAT(ROUND(SUM(DATA_LENGTH/1024/1024),2),'MB') as data from information_schema.TABLES where table_schema='%s' and table_name='%s'; ''' % (self.DatabaseName, self.TableName)
        return self.__Execute(SQL)[0][0]


def SQLString(String):
    return '\'' + String + '\''


class UpdateManager:
    def __init__(self, DatabaseTable):
        self.DatabaseTable = DatabaseTable
        self.DatabaseTable.CheckColumn({
            'ItemIDX': 'BIGINT NOT NULL',
            'ItemName': 'CHAR(64) NOT NULL',
            'UpdateTime': 'CHAR(16) NOT NULL',
        }, Index={'ItemIndex':['ItemIDX', 'ItemName']})


    def Update(self, Name):
        Recode = self.DatabaseTable.SearchID('''WHERE ItemIDX=CRC32('%s') AND ItemName='%s' ''' % (Name, Name))
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

    def TableUpdateTime(self, Name):
        Result = self.DatabaseTable.SearchTable('''WHERE ItemIDX=CRC32('%s') AND ItemName='%s' ''' % (Name, Name))
        if len(Result) == 0:
            return None
        else:
            return Date(Result[0][3])
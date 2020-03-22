import pymysql
import os, sys

from PyBear.GlobalBear import *

class DatabaseTable():
    def __init__(self, ServerName, UserName, DatabaseName, TableName):
        self.Connection = pymysql.connect(
            host=GetServer(ServerName).IP,
            port=GetServer(ServerName).Port,
            user=GetUser(UserName).UserName,
            passwd=GetUser(UserName).Password,
            db=DatabaseName,)
        self.TableName = TableName
        self.Cursor = self.Connection.cursor()

        Tables = [Item[0] for Item in self.__Execute('''SHOW TABLES;''')]
        if self.TableName not in Tables:
            SQL = '''CREATE TABLE %s (ID INT AUTO_INCREMENT, PRIMARY KEY(ID)) CHARSET=utf8;''' % (self.TableName)
            self.__Execute(SQL)

        self.ListColumn()
    
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
        self.ListColumn()

    def AddUniqueIndex(self):
        pass

    def AddFulltextIndex(self):
        pass

    def ListColumn(self):
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
        print(ColumnName)
        for Item in ColumnName:
            if Item not in self.Columns:
                return
        
        ColumnName = ','.join(ColumnName)

        for Item in Data:
            Item = ','.join(['\''+Value+'\'' for Value in Item if type(Value) == str])
            SQL = '''INSERT INTO %s (%s) VALUES (%s);''' % (self.TableName, ColumnName, Item)
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

    def Change(self, CColumnName, CValue, TColumnName, TValue):
        if CColumnName not in self.Columns or TColumnName not in self.Columns:
            return

        if type(CValue) == str:
            CValue = '\'' + CValue + '\''
        if type(TValue) == str:
            TValue = '\'' + TValue + '\''
        SQL = '''UPDATE %s SET %s = %s WHERE %s = %s;''' % (TableName, TColumnName, TValue, CColumnName, CValue)
        self.__Execute(SQL)



    def ListTable(self): 
        return self.__Execute('''SELECT * FROM %s''' % (self.TableName))

    def SearchTable(self, ColumnName, Value):
        if ColumnName not in self.Columns:
            return ()

        if type(Value) == int:
            SQL = '''select * from %s where %s = %s ''' % (self.TableName, ColumnName, Value)
        else:
            SQL = '''select * from %s where %s = '%s' ''' % (self.TableName, ColumnName, Value)
        return self.__Execute(SQL)

    def SearchID(self, ColumnName, Value):
        return [Item[0] for Item in self.SearchTable(ColumnName, Value)]


    def Distinct(self, ColumnName):
        SQL = '''DELETE %s FROM %s, (SELECT min(id) AS mid, %s FROM %s GROUP BY %s) AS t2 WHERE %s.id != t2.mid;''' % (self.TableName, self.TableName, ColumnName, self.TableName, ColumnName, self.TableName)
        self.__Execute(SQL)
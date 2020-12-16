import pymysql
import os, sys

import PyBear.Bear as Bear

class MySQL:
    def __init__(self, ServerName, DatabaseName, TableName=None):
        self.ServerName = ServerName
        self.DatabaseName = DatabaseName
        self.TableName = TableName

        self.Connection = pymysql.connect(
            host=GetServer(ServerName).IP,
            port=GetServer(ServerName).Port,
            user=GetServer(ServerName).UserName,
            passwd=GetServer(ServerName).Password,
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



    def ListTable(self):
        SQL = ''' SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='%s'; ''' % (self.DatabaseName)
        return [Item[0] for Item in self.__Execute(SQL)]

    def InitDatabase(self, TableList):
        ServerTableList = self.ListTable()
        for Item in TableList:
            if Item not in ServerTableList:
                SQL = '''CREATE TABLE %s (ID INT AUTO_INCREMENT, PRIMARY KEY(ID)) CHARSET=utf8;''' % (Item)
                self.__Execute(SQL)
    
    def DeleteTable(self, Condition):
        SQL = '''select concat('drop table ', table_name, ';') from information_schema.tables where table_name like '%s';''' % (Condition)
        for SQL in self.__Execute(SQL):
            print(SQL)
            self.__Execute(SQL[0])



    def QuickInit(self, Columns, Index=None, UniqueIndex=None, FulltextIndex=None):
        if not self.TableName:
            return 'No TableName'
        if self.TableName in self.ListTable():
            return
        self.InitDatabase(self.TableName)
        self.InitTable(self, Columns, Index=Index, UniqueIndex=UniqueIndex, FulltextIndex=FulltextIndex)



    def InitTable(self, Columns, Index=None, UniqueIndex=None, FulltextIndex=None):
        if not self.TableName:
            return 'No TableName'

        self.Cursor.execute('''TRUNCATE TABLE %s;''' % (self.TableName))
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
        if not self.TableName:
            return 'No TableName'
            

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



    def Search(self, Column='*', Condition=''):
        if not self.TableName:
            return 'No TableName'
              
        return self.__Execute('''SELECT %s FROM %s %s''' % (Column, self.TableName, Condition))


    def Distinct(self, ColumnName):
        SQL = '''DELETE %s FROM %s, (SELECT min(id) AS mid, %s FROM %s GROUP BY %s) AS t2 WHERE %s.id != t2.mid;''' % (self.TableName, self.TableName, ColumnName, self.TableName, ColumnName, self.TableName)
        self.__Execute(SQL)

    def GetTableSize(self):
        SQL = ''' SELECT DATA_LENGTH as data from information_schema.TABLES where table_schema='%s' and table_name='%s'; ''' % (self.DatabaseName, self.TableName)
        Ret = self.__Execute(SQL)
        if len(Ret) == 0:
            return None
        else:
            return Ret[0][0]

    def GetRowNumber(self):
        SQL = '''SELECT MAX(ID) FROM %s;''' % (self.TableName)
        Ret = self.__Execute(SQL)
        if len(Ret) == 0:
            return None
        else:
            return Ret[0][0]
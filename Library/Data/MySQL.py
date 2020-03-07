import pymysql
import os, sys

from PyBear.GlobalBear import *

DatabasesServers = {}
def NewDatabasesServer(Name, Username, Password, Ip='127.0.0.1', Port=3306):
    DatabasesServer[Name] = [Username, Password, Ip, Port]

class Database():
    def __init__(self, ServerName, DatabaseName):
        self.Connection = pymysql.connect(
            host=DatabasesServer[ServerName][2],
            port=DatabasesServer[ServerName][3],
            user=DatabasesServer[ServerName][0],
            passwd=DatabasesServer[ServerName][1],
            db=DatabaseName,)
        self.Cursor = self.Connection.cursor()
    
    def ShowResult(self):
        return self.Cursor.fetchall()


    def NewTable(self, TableName):
        if self.ListTable().count(TableName) != 0:
            return False
        _SQL = '''Create Table %s (id int AUTO_INCREMENT, primary key(id)) charset=utf8;''' % (TableName)
        self.Cursor.execute(_SQL)
        self.Connection.commit()
        return True

    def DropTable(self, TableName):
        _SQL = '''drop table %s;''' % (TableName)
        self.Cursor.execute(_SQL)
        self.Connection.commit()

    def ListTable(self):
        _SQL = '''show tables;'''
        self.Cursor.execute(_SQL)
        return self.ShowResult()[0]


    def NewColumn(self, TableName, name):
        if self.ListColumn(TableName).count(name) != 0:
            return -1
        _SQL = '''alter table %s add %s char(255);''' % (TableName, name)
        self.Cursor.execute(_SQL)
        self.Connection.commit()
        return 1

    def DropColumn(self, TableName, name):
        if self.ListColumn(TableName).count(name) == 0:
            return -1
        _SQL = '''alter table %s drop %s;''' % (TableName, name)
        self.Cursor.execute(_SQL)
        self.Connection.commit()
        return 1

    def ListColumn(self, TableName, Raw=False):
        _SQL = '''show COLUMNS from %s''' % (TableName)
        self.Cursor.execute(_SQL)
        if Raw:
            return self.ShowResult()
        else:
            return [Item[0] for Item in self.ShowResult()]


    def Insert(self, TableName, dictionary):
        self.NewTable(TableName)
        _field = ''
        _value = ''
        _counter = 0
        for item in dictionary:
            if _counter != 0:
                _field += ','
                _value += ','
            _field += item
            _value += ''''%s' ''' % (dictionary[item])
            _counter += 1
        for item in _field.split(','):
            self.NewColumn(TableName, item)      
        _SQL = '''INSERT INTO %s (%s) VALUES (%s);''' % (TableName, _field, _value)
        self.Cursor.execute(_SQL)
        self.Connection.commit()
    
    def Delete(self, TableName, id):
        _SQL = '''DELETE FROM %s WHERE id = %s;''' % (TableName, id)
        self.Cursor.execute(_SQL)
        self.Connection.commit()

    def Change(self, TableName, A, B, Column, to):
        self.NewColumn(TableName, Column)
        _SQL = '''UPDATE %s SET %s = '%s' WHERE %s = '%s';''' % (TableName, Column, to, A, B)
        self.Cursor.execute(_SQL)
        self.Connection.commit()

    def List(self, TableName): 
        _SQL = '''SELECT * FROM %s''' % (TableName)
        self.Cursor.execute(_SQL)
        return self.ShowResult()

    def Search(self, TableName, Src, Des):
        try:
            if type(Des) == int:
                _SQL = '''select * from %s where %s = %s ''' % (TableName, Src, Des)
            else:
                _SQL = '''select * from %s where %s = '%s' ''' % (TableName, Src, Des)
            self.Cursor.execute(_SQL)
            return self.ShowResult()
        except Exception as e:
            print('SearchTable Error')
            return ()


    def Exec(self, SQL):
        self.Cursor.execute(_SQL)
        return self.ShowResult()

    def Distinct(self, TableName, colunm):
        _SQL = '''delete %s from %s, (select min(id) as mid, %s from %s group by %s) as t2 where %s.id != t2.mid;''' % (TableName, TableName, colunm, TableName, colunm, TableName)
        print (_SQL)
        return
        self.Cursor.execute(_SQL)
        self.Connection.commit()
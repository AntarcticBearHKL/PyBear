import os, sys

import PyBear.GlobalBear as GlobalBear
import PyBear.Library.Data.MySQL as MySQLBear
import PyBear.Library.Chronus as ChronusBear

def InitWebDisk(DatabaseName, TableName):
    pass

def UploadFile(DatabaseName, TableName, Directory, BinFile):
    pass

def DeleteFile(DatabaseName, TableName, Directory):
    pass

def DownloadFile(DatabaseName, TableName, Directory):
    pass

def DirectorySplit(Directory):
    return os.path.dirname(Directory), os.path.basename(Directory)
import sys,os

from PyBear.GlobalBear import *

def WriteU(Path, content):
    if not os.path.exists(os.path.dirname(Path)):
        os.makedirs(os.path.dirname(Path))
    file = open(Path, 'w', encoding='utf-8')
    file.write(content)
    file.close()

def ReadU(Path):
    if not os.path.exists(Path):
        print('File: ' + Path + ' Not Exist')
        return ''
    retf = open(Path, 'r', encoding='utf-8')
    Ret = retf.read()
    retf.close()
    return Ret

def WriteB(Path, content):
    if not os.path.exists(os.path.dirname(Path)):
        os.makedirs(os.path.dirname(Path))
    file = open(Path, 'wb')
    file.write(content)
    file.close()

def ReadB(Path):
    if not os.path.exists(Path):
        print('File: ' + Path + ' Not Exist')
        return ''
    retf = open(Path, 'rb')
    Ret = retf.read()
    retf.close()
    return Ret

def Read(Path):
    try:
        return ReadU(Path)
    except:
        return ReadB(Path)

Write = WriteU


def NewFile(Path):
    Write(Path, '')

NewDirectory = os.makedirs


def List(Path):
    return os.listdir(Path)

def DetailList(Path):
    Ret = {}
    for node in flist(Path):
        if os.path.isfile(fjoin(Path, node)):
            Ret[node] = 'file'
        else:
            Ret[node] = 'directory'
    return Ret


def Removefile(Path):
    if fexists(Path):
        os.remove(Path)
        return True
    else:
        return False

def RemoveDirectory(Path):
    for root, dirs, files in os.walk(Path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

Rename = os.rename

Exists = os.path.exists
Join = os.path.join

IsFile = os.path.isfile
IsDirectory = os.path.isdir
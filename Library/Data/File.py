import sys,os

from PyBear.GlobalBear import *

def FUWrite(Path, content):
    if not os.path.exists(os.path.dirname(Path)):
        os.makedirs(os.path.dirname(Path))
    file = open(Path, 'w', encoding='utf-8')
    file.write(content)
    file.close()

def FURead(Path):
    if not os.path.exists(Path):
        print('File: ' + Path + ' Not Exist')
        return ''
    retf = open(Path, 'r', encoding='utf-8')
    Ret = retf.read()
    retf.close()
    return Ret

def FBWrite(Path, content):
    if not os.path.exists(os.path.dirname(Path)):
        os.makedirs(os.path.dirname(Path))
    file = open(Path, 'wb')
    file.write(content)
    file.close()

def FBRead(Path):
    if not os.path.exists(Path):
        print('File: ' + Path + ' Not Exist')
        return ''
    retf = open(Path, 'rb')
    Ret = retf.read()
    retf.close()
    return Ret

def FRead(Path):
    try:
        return FURead(Path)
    except:
        return FBRead(Path)

FWrite = FUWrite


def FNewFile(Path):
    FWrite(Path, '')

FNewDirectory = os.makedirs


def FList(Path):
    return os.listdir(Path)

def FDetailList(Path):
    Ret = {}
    for node in flist(Path):
        if os.path.isfile(fjoin(Path, node)):
            Ret[node] = 'file'
        else:
            Ret[node] = 'directory'
    return Ret


def FRemovefile(Path):
    if fexists(Path):
        os.remove(Path)
        return True
    else:
        return False

def FRemoveDirectory(Path):
    for root, dirs, files in os.walk(Path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

FRename = os.rename

FExists = os.path.exists
FJoin = os.path.join

FIsFile = os.path.isfile
FIsDirectory = os.path.isdir
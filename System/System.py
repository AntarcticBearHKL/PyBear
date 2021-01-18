import PyBear.Bear as Bear

from pip._internal.utils.misc import get_installed_distributions 
from subprocess import call
import os

def ClearScreen():
    os.system('cls')

def InitEnvironment():
    import platform
    if platform.system() == "Windows":
        pass
    elif platform.system() == "Linux":
        os.system("tar -xvf /Bear/Shell/talib.tar.gz")
        os.system("cd ta-lib")
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("make install")
        os.system("cd ..")
        os.system("rm talib.tar.gz")
        os.system("rm -rf ta-lib")
    
    os.system('pip3 install --upgrade pip')
    for Module in Bear.BearModule:
        print('Installing: ', Module)
        os.system("pip3 install " + Module)

def UpgradeEnvironment():
    os.system('pip3 install --upgrade pip')
    for dist in get_installed_distributions():
        print('Upgrade: ', dist.project_name)
        os.system("pip3 install --upgrade " + dist.project_name)

exit()
import PyBear.System.System as S
S.InitEnvironment()
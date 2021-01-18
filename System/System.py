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

    for Module in Bear.BearModule:
        print(Module)
        os.system('python -m pip install --upgrade pip')
        os.system("pip3 install " + Module)

def UpgradeEnvironment():
    for dist in get_installed_distributions():
        os.system('python -m pip install --upgrade pip')
        os.system("pip3 install --upgrade " + dist.project_name)
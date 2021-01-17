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
        os.system("apt install curl")
        os.system("curl http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz")
        os.system("tar -xzvf ta-lib-0.4.0-src.tar.gz")
        os.system("cd ta-lib")
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("make install")
        os.system("cd ..")
        os.system("rm ta-lib-0.4.0-src.tar.gz")
        os.system("rm ta-lib")

    for Module in Bear.BearModule:
        print(Module)
        os.system('python.exe -m pip install --upgrade pip')
        os.system("pip3 install " + Module, shell=True)

def UpgradeEnvironment():
    for dist in get_installed_distributions():
        os.system('python.exe -m pip install --upgrade pip')
        os.system("pip3 install --upgrade " + dist.project_name)
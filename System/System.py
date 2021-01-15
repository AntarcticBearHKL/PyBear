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
        '''
        call("apt install curl")
        call("curl http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz")
        call("tar -xzvf ta-lib-0.4.0-src.tar.gz")
        call("cd ta-lib")
        call("./configure --prefix=/usr")
        call("make")
        call("make install")
        call("cd ..")
        call("rm ta-lib-0.4.0-src.tar.gz")
        call("rm ta-lib")
        '''

    for Module in Bear.BearModule:
        print(Module)
        call("pip3 install " + Module, shell=True)

def UpgradeEnvironment():
    for dist in get_installed_distributions():
        call("pip3 install --upgrade " + dist.project_name, shell=True)
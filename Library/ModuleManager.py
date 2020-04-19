from PyBear import GlobalBear

from pip._internal.utils.misc import get_installed_distributions 
from subprocess import call

def UpgradeModule():
    for dist in get_installed_distributions():
        call("pip3 install --upgrade " + dist.project_name, shell=True)

def InstallAll():
    for Module in GlobalBear.ModuleList:
        print(Module)
        call("pip3 install " + Module, shell=True)
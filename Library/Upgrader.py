from pip._internal.utils.misc import get_installed_distributions 
from subprocess import call

def UpgradeLibrary():
    for dist in get_installed_distributions():
        call("pip install --upgrade " + dist.project_name, shell=True)

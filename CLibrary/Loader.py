import ctypes 

from PyBear.GlobalBear import *

def LoadCLib(libname):
    return ctypes.CDLL(libname)   
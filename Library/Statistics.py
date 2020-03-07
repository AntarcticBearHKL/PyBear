import sys,os
import scipy
import numpy
import math

from PyBear.GlobalBear import *

def BMean(Input):
    return numpy.array(Input).mean()

def BStd(Input, DDOF=1):
    return numpy.array(Input).std(ddof=DDOF)

def BVar(Input, DDOF=1):
    return numpy.array(Input).std(ddof=DDOF) ** 2


def BCov(InputA, InputB):
    return numpy.cov(InputA, InputB)[0,1]

def BCorr(InputA, InputB):
    return numpy.corrcoef(InputA, InputB)[0,1]


def BCovMAT(InputA, InputB):
    return numpy.cov(InputA, InputB)

def BCorrMAT(InputA, InputB):
    return numpy.corrcoef(InputA, InputB, InputA, InputA)
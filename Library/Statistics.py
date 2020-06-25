import sys,os
import scipy
import numpy
import math

import PyBear.GlobalBear as GlobalBear

def Mean(Input):
    return numpy.array(Input).mean()

def Std(Input, DDOF=1):
    return numpy.array(Input).std(ddof=DDOF)

def Var(Input, DDOF=1):
    return numpy.array(Input).std(ddof=DDOF) ** 2


def Cov(InputA, InputB):
    return numpy.cov(InputA, InputB)[0,1]

def Corr(InputA, InputB):
    return numpy.corrcoef(InputA, InputB)[0,1]


def CovMAT(InputA, InputB):
    return numpy.cov(InputA, InputB)

def CorrMAT(InputA, InputB):
    return numpy.corrcoef(InputA, InputB, InputA, InputA)
from PyBear.GlobalBear import *

def CompoundInterestPresent():
    pass

def CompoundInterestFinal():
    pass

def AnnuityPresent(PaidPerYear, Year, InterestRate):
    Ret = []
    for Counter in range(Year):
        Ret.append( PaidPerYear / ((1+InterestRate) ** (Counter+1)) )
    return Ret

def AnnuityFinal(PaidPerYear, Year, InterestRate):
    Ret = []
    for Counter in range(Year):
        Ret.append( PaidPerYear * ((1+InterestRate) ** (Counter)) )
    Ret.reverse()
    return Ret

def BondPresent(Principal, BondInterestRate, Year, InterestRate):
    Ret = AnnuityPresent(Principal*BondInterestRate, Year, InterestRate)
    Ret.append((Principal/((1+InterestRate)**Year)))
    return Ret
 
def Perpetuities():
    pass

def CompoundingInterestRates():
    pass 
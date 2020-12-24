import PyBear.Bear as Bear
import PyBear.System.Chronus as Cr

Para_Money = -1
Para_Date = -2
Para_String = -3

ModuleList = {}
def NewModule(Module):
    ModuleList[Module.Name] = [list(Module.Code), Module]

@Bear.CatchBadBear
def Cast(Input):
    Input = str(Input)
    if len(Input)<4:
        Code = '0'*(4-len(Input[0])) + Input
        Para = ''
    else:
        Code = Input[:4]
        Input = Input[4:]
    for Item in ModuleList:
        if Code in ModuleList[Item][0]:
            return ModuleList[Item][1].Run(Code, Input)
        else:
            return Bear.Result(0, 'Code Not Exist')

class Core:
    def __init__(self):
        self.Name = 'Default'
        self.Code = {}
        self.Input = None
    
    def Run(self, Code, Input):
        self.Input = Input
        return self.Code[str(Code)]()

    def GetParameter(self, ParameterList, InputCheck = None):
        Ret = []
        if len(self.Input) <= 0:
            raise Bear.BadBear('Input Error')

        for Parameter in ParameterList:
            if Parameter > 0: #标准读取
                Ret.append(self.ParaDefault(Parameter))
            elif Parameter == Para_Date: # 日期输入
                Ret.append(self.ParaDate())
            elif Parameter == Para_Money: # 金额输入
                Ret.append(self.ParaMoney())
            elif Parameter == Para_String: # 字符输入
                Ret.append(self.ParaString())
        
        return Ret

    def ParaDefault(self, Num):
        Ret = self.Input[:Num]
        if Ret.count('.'):
            raise Bear.BadBear('Input Error')
        self.Input = self.Input[Num:]
        return Ret

    def ParaDate(self):
        Counter = 0
        while self.Input[Counter] != '.':
            Counter += 1
            if Counter == 14:
                break

        if Counter == 0:
            Para = 0
            self.Input = self.Input[1:]
        elif Counter == 14:
            Para = int(self.Input[:14])
            self.Input = self.Input[14:]
        else:
            Para = int(self.Input[:Counter])
            self.Input = self.Input[Counter+1:]

        if Para == 0:
            return Cr.Date().String(-2)
        elif 0 < Para < 10:
            return Cr.Date().Shift(Day=Para).String(-2)
        elif 10< Para < 20:
            return Cr.Date().Shift(Day=-Para+10).String(-2)
        elif len(str(Para)) == 8:
            return Cr.Date(str(Para)).String(-2)
        elif len(str(Para)) == 14:
            return Cr.Date(str(Para)).String(-2)
        else:
            raise Bear.BadBear('Input Error')

    def ParaMoney(self):
        Counter = 0
        while self.Input[Counter] != '.':
            Counter += 1
        Ret = self.Input[:Counter]
        self.Input = self.Input[Counter+1:]
        return str((int(Ret))/100)

    def ParaString(self):
        Counter = 0
        while self.Input[Counter] != '/':
            Counter += 1
        Ret = self.Input[:Counter]
        self.Input = self.Input[Counter+1:]
        return str(Ret)
                

import PyBear.TimeCapsule.Account as Account
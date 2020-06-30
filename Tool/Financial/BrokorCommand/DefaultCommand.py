import PyBear.GlobalBear as GlobalBear
from PyBear.Tool.Financial.Brokor import BrokorCommand

def Load(Brokor):
    CommandLAST().Init(Brokor)
    CommandNext().Init(Brokor)
    CommandPS().Init(Brokor)

class CommandLAST(BrokorCommand):
    def __init__(self):
        self.Name = ['LAST', 'L']

    def CommandFunction(self, ParameterList):
        if self.Brokor.Pointer > self.Brokor.PointerMargin[0]:
            self.Brokor.Pointer -= 1
        else:
            print('THIS IS THE FIRST DAY.')
            input('PRESS BUTTON TO CONTINUE...')

class CommandNext(BrokorCommand):
    def __init__(self):
        self.Name = ['NEXT', 'N']

    def CommandFunction(self, ParameterList):
        if self.Brokor.Pointer < self.Brokor.PointerMargin[1]:
            self.Brokor.Pointer += 1
        else:
            print('THIS IS THE LAST DAY.')
            input('PRESS BUTTON TO CONTINUE...')

class CommandPS(BrokorCommand):
    def __init__(self):
        self.Name = ['PS', 'P']

    def CommandFunction(self, ParameterList):
        for Item in self.Brokor.Data:
            print(Item, ': ', self.Brokor.Data[Item][self.Brokor.Pointer])
        input('PRESS BUTTON TO CONTINUE...')
import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self, Brokor):
        self.LeftMargin = 1
        Brokor.Data['StrategyAlpha'] = [None] * self.LeftMargin
        Brokor.Result['StrategyAlpha'] = []
        
    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.g('KDJF', -1) < b.g('KDJS', -1),
                b.g('KDJF', 0) > b.g('KDJS', 0),
            ],
        ])
        if ConditionA:
            b.Data['StrategyAlpha'].append(1)
            b.Recommend()
        else:
            b.Data['StrategyAlpha'].append(None)
import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        self.LeftMargin = 1
        #self.Brokor.NewEmptyList('StrategyAlpha', self.LeftMargin)
        self.Brokor.NewResult('StrategyAlpha')
        
    def TraversalFunction(self, b):
        return
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
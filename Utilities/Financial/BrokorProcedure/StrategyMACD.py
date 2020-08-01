import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        self.LeftMargin = 1
        self.Brokor.NewEmptyList('StrategyMACD', self.LeftMargin)
        
    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.d('DIF', 0) > b.d('DEA', 0),
                b.d('DIF', 0) > 0,
                b.d('DEA', 0) > 0,
                b.d('MACDMX', 0) == 1,
            ],
        ])
        ConditionB = b.j([
            [
                b.d('DIF', -1) > b.d('DEA', -1),
                b.d('DIF', -1) > 0,
                b.d('DEA', -1) > 0,
                b.d('MACDMX', -1) == 1,
            ],
        ])
        ConditionC = b.j([
            [
                b.d('MACDMX', 0) == -1,
            ],
        ])
        if ConditionA:
            b.Data['StrategyMACD'].append(1)
        elif ConditionB:
            b.Data['StrategyMACD'].append(2)
        elif ConditionC:
            b.Data['StrategyMACD'].append(-1)
        else:
            b.Data['StrategyMACD'].append(0)
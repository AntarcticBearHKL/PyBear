import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self, Brokor):
        KDJF, KDJS = talib.STOCH(
            numpy.array(self.Input('High')),
            numpy.array(self.Input('Low')),
            numpy.array(self.Input('Close')),
            fastk_period = self.GetConfigInt('FastK', '22'),
            slowk_period = self.GetConfigInt('SlowK', '5'),
            slowk_matype = 0,
            slowd_period = self.GetConfigInt('SlowD', '5'),
            slowd_matype = 0,)

        self.Output('KDJF', KDJF)
        self.Output('KDJS', KDJS)

        self.LeftMargin = 2
        self.Brokor.NewEmptyList('KDJX', self.LeftMargin)

    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.d('KDJX', -1) < 0,
                b.d('KDJX', -0) > 0,
            ],
        ])
        ConditionB = b.j([
            [
                b.d('KDJX', -2) < 0,
                b.d('KDJX', -1) > 0,
            ],
        ])
        ConditionC = b.j([
            [
                b.d('KDJX', -2) > 0,
                b.d('KDJX', -1) < 0,
            ],
        ])
        if ConditionA:
            b.Data['MACDMX'].append(1)
        elif ConditionB:
            b.Data['MACDMX'].append(2)
        elif ConditionC:
            b.Data['MACDMX'].append(-1)
        else:
            b.Data['MACDMX'].append(0)
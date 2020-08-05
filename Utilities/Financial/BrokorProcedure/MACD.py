import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        DIF, DEA, NOIR = talib.MACD(
            numpy.array(self.Input('Close')),
            fastperiod=self.GetConfigInt('Fast', '5'), 
            slowperiod=self.GetConfigInt('Slow', '22'), 
            signalperiod=self.GetConfigInt('Signal', '9'))
        MACD = DIF - DEA

        MACDM = talib.MA(
            numpy.array(MACD),
            timeperiod=10,
        )

        MACDM = (MACD - MACDM) * 10

        self.Output('DIF', DIF)
        self.Output('DEA', DEA)
        self.Output('MACD', MACD)
        self.Output('MACDM', MACDM)

        self.LeftMargin = 2
        self.Brokor.NewEmptyList('MACDMX', self.LeftMargin)

    def TraversalFunction(self, b):
        ConditionA = b.j([
            [
                b.d('MACDM', -1) < 0,
                b.d('MACDM', -0) > 0,
            ],
        ])
        ConditionB = b.j([
            [
                b.d('MACDM', -2) < 0,
                b.d('MACDM', -1) > 0,
            ],
        ])
        ConditionC = b.j([
            [
                b.d('MACDM', -2) > 0,
                b.d('MACDM', -1) < 0,
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
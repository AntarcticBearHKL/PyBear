import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self, Brokor):
        self.LeftMargin = 1
        Brokor.NewEmptyList('StrategyAlpha', self.LeftMargin)
        Brokor.NewResult('StrategyAlpha')
        
        Brokor.RequireData(['Close'])
        DIF, DEA, MACD = talib.MACD(
            numpy.array(Brokor.GetData('Close')),
            fastperiod=self.GetConfigInt('Fast', '5'), 
            slowperiod=self.GetConfigInt('Slow', '22'), 
            signalperiod=self.GetConfigInt('Signal', '9'))

        Brokor.ProvideData({
            'DIF': DIF,
            'DEA': DEA,
            'MACD': MACD*2,})

    def TraversalFunction(self, b):
        pass
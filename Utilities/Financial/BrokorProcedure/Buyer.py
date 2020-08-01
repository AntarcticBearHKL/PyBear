import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        self.LeftMargin = 1
        self.Brokor.NewResult('Buyer')
        
    def TraversalFunction(self, b):
        
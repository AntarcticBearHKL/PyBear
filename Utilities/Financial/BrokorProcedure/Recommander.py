import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        if self.Brokor.Data[self.GetConfig('Target')][-1] == 1:
            self.Brokor.Recommend()
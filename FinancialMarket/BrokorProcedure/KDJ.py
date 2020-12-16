import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

def SMA(Input, N, M):
    Ret = 0
    result=[]
    for Item in Input:
        if np.isnan(Item):
            Item = np.nan_to_num(Item)
            Ret = (m*Item +(n-m)*Ret) / n
            result.append(Ret)
    return np.array(result)

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        tp = 3
        KDJF, KDJS = talib.STOCH(
            numpy.array(self.Input('High')),
            numpy.array(self.Input('Low')),
            numpy.array(self.Input('Close')),
            fastk_period = self.GetConfigInt('FastK', '22'),
            slowk_period = self.GetConfigInt('SlowK', '5'),
            slowk_matype = tp,
            slowd_period = self.GetConfigInt('SlowD', '5'),
            slowd_matype = tp,)

        self.Output('KDJF', KDJF)
        self.Output('KDJS', KDJS)
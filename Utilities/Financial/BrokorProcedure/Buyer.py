import talib
import numpy

import PyBear.GlobalBear as GlobalBear
import PyBear.Utilities.Financial.Brokor as BrokorBear

class Config(BrokorBear.BrokorProcedure):
    def Run(self):
        self.LeftMargin = 0
        self.Brokor.NewResult('Buyer')

        self.Hold = False
        self.Asset = self.GetConfigInt('Asset')

        self.Info = {}
        self.HighestPrice = None
        self.LowestPrice = None

    def Buy(self, Date, Price, High, Low):
        BuyNum = (self.Asset // (Price * 100)) * 100
        if not BuyNum:
            return
        TotalBuyValue = BuyNum * Price
        if TotalBuyValue > 20000:
            BuyTax = TotalBuyValue * 0.00025
        else:
            BuyTax = 5
        self.Info['BuyDate'] = Date
        self.Info['BuyNum'] = BuyNum
        self.Info['BuyPrice'] = Price
        self.Info['TotalBuyValue'] = TotalBuyValue
        self.Info['BuyTax'] = BuyTax
        self.Hold = True

        self.HighestPrice = float(High)
        self.LowestPrice = float(Low)

    def Log(self, Date, High, Low):
        if float(High) > self.HighestPrice:
            self.HighestPrice = float(High)
        if float(Low) < self.LowestPrice:
            self.LowestPrice = float(Low)

    def Sell(self, Date, Price):
        TotalSellValue = Price * self.Info['BuyNum']
        if TotalSellValue > 20000:
            SellTax = TotalSellValue * (0.00025 + 0.001)
        else:
            SellTax = 5 + TotalSellValue * 0.001

        self.Info['Highest'] = self.HighestPrice
        self.Info['Lowest'] = self.LowestPrice

        self.Info['SellDate'] = Date
        self.Info['SellNum'] = self.Info['BuyNum']
        self.Info['SellPrice'] = Price
        self.Info['TotalSellValue'] = TotalSellValue
        self.Info['SellTax'] = SellTax

        self.Info['Profit'] = TotalSellValue - self.Info['TotalBuyValue'] - SellTax - self.Info['BuyTax']
        self.Info['ProfitP'] = round((self.Info['Profit'] / self.Info['TotalBuyValue']), 4) * 100

        self.Brokor.Result['Buyer'].append(self.Info)
        self.HighestPrice = None
        self.LowestPrice = None
        self.Info = {}
        self.Hold = False
        
    def TraversalFunction(self, b):
        if self.Hold:
            if b.d(self.GetConfig('Target'), 0) == -1:
                self.Sell(b.t(0), b.d('Open', 0))
            else:
                self.Log(b.t(0), b.d('High', 0), b.d('Low', 0))
        elif b.d(self.GetConfig('Target'), 0) == 2:
            self.Buy(b.t(0), b.d('Open', 0), b.d('High', 0), b.d('Low', 0))
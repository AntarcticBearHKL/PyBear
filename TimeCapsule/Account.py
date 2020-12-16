import PyBear.Bear as Bear
import PyBear.System.Chronus as Cr
import PyBear.TimeCapsule.Core as Core
import PyBear.DataBase.MongoDB as Mongo

class Account(Core.Core):
    def __init__(self):
        Core.Core.__init__(self)
        self.Name = 'Account'
        self.Code = {
            '6101': self.FN6101, # 开立新账
            '6102': self.FN6102, # 记借方
            '6103': self.FN6103, # 记贷方
            '6106': self.FN6606, # 记账登记
            '6107': self.FN6607, # 登记记账

            '6601': self.FN6601, # 记账登记
            '6602': self.FN6602, # 记借方
            '6603': self.FN6603, # 记贷方
            '6606': self.FN6606, # 记账

            '6701': self.FN6701, # 查询现金余额
            '6721': self.FN6721, # 查询当日损益
            '6725': self.FN6725, # 查询时段损益数据

            '6999': self.FN6999, # 汇总账
        }

    def FN6101(self):
        Code, Type, Name = self.GetParameter([4, 1, 'Name'])
        #Code: 账户类型/分账序号/账目序号
        #Type: 1资产 2负债 3权益

        DB = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        if DB.Search({'AccountCode': Code}, Count= True):
            return Bear.Result(-1, 'Account Already Exist')

        DB.Insert({
            'Code': str(Code),
            'Name': str(Name),
            'Type': str(Type),
            'Amount': float(0.00),
        })
        return Bear.Result(1, 'Account Create Success')

    def FN6102(self):
        Code, Period, Date, Amount, Label, Remark = self.GetParameter([4, 4, -1, -2, 'Label', 'Remark'])

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] != 1:
            Amount = -Amount
        
        AccountAmount = float(AccountInfo['Amount'])

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'Date': str(Date),
            'DateInt': int(Date[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Period': int(Period),
            'Remark': str(Remark),
        })
        BalanceSheet.Change({'Code': str(Code)},{
            '$set': {'Amount': AccountAmount + Amount}
        })

    def FN6103(self):
        Code, Period, Date, Amount, Label, Remark = self.GetParameter([4, 4, -1, -2, 'Label', 'Remark'])

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] == 1:
            Amount = -Amount

        AccountAmount = float(AccountInfo['Amount'])

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'Date': str(Date),
            'DateInt': int(Date[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Period': int(Period),
            'Remark': str(Remark),
        })
        BalanceSheet.Change({'Code': str(Code)},{
            '$set': {'Amount': AccountAmount + Amount}
        })


    def FN6106(self):
        print('Success')


    def FN6602(self):
        Code, Amount, Label = self.GetParameter([4, -2, 'Label'])

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] != 1:
            Amount = -Amount

        Date = Cr.Date().String(-2)
        Period = 1
        Remark = '借记'

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'Date': str(Date),
            'DateInt': int(Date[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Period': int(Period),
            'Remark': str(Remark),
        })

    def FN6603(self):
        Code, Amount, Label= self.GetParameter([4, -2, 'Label'])

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] == 1:
            Amount = -Amount

        Date = Cr.Date().String(-2)
        Period = 1
        Remark = '贷记'

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'Date': str(Date),
            'DateInt': int(Date[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Period': int(Period),
            'Remark': str(Remark),
        })


    def FN6701(self):
        print('Success')


    def FN6721(self):
        print('Success')
 
    def FN6725(self):
        print('Success')

    def FN6999(self):
        print('Success')

Core.NewModule(Account())
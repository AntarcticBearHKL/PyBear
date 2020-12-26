import PyBear.Bear as Bear
import PyBear.System.Chronus as Cr
import PyBear.TimeCapsule.Core as Core
import PyBear.Database.MongoDB as Mongo

class Account(Core.Core):
    def __init__(self):
        Core.Core.__init__(self)
        self.Name = 'Account'
        self.Code = {
            '6001': self.FN6001, # 汇总账
            '6002': self.FN6002, # 轧差对账
            '6060': self.FN6060, # 余额查询

            '6101': self.FN6101, # 开立账户
            '6102': self.FN6102, # 记借方
            '6103': self.FN6103, # 记贷方
            '6105': self.FN6105, # 销记账户
            '6106': self.FN6106, # 转账

            '6606': self.FN6606, # 查询流水
            '6625': self.FN6621, # 查询时段损益数据

            '6901': self.FN6901, # 新建标签
            '6906': self.FN6906, # 标签信息显示
        }

    def FN6001(self):
        DB = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')
        Ret = {'资产账户':[], '负债账户':[], '权益账户':[]}
        Debit = DB.Search({'Type':'1'}, Sort=['Code', 1])
        for Line in Debit:
            Ret['资产账户'].append([Line['Code'], Line['Name'], Line['Amount']])

        Debit = DB.Search({'Type':'2'}, Sort=['Code', 1])
        for Line in Debit:
            Ret['负债账户'].append([Line['Code'], Line['Name'], Line['Amount']])

        Debit = DB.Search({'Type':'3'}, Sort=['Code', 1])
        for Line in Debit:
            Ret['权益账户'].append([Line['Code'], Line['Name'], Line['Amount']])
        return Ret

    def FN6002(self):
        DB = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet').Search({})
        DebitAmount = 0
        CreditAmount = 0

        for Item in DB:
            if Item['Type'] == '1':
                DebitAmount += Item['Amount']
            else:
                CreditAmount += Item['Amount']
        Difference = round(DebitAmount - CreditAmount, 2)
        if Difference >= 0:
            Difference = '+ ' + str(Difference)
        else:
            Difference = '- ' + str(Difference)
        return [DebitAmount, CreditAmount, Difference]

    def FN6060(self):
        print('Success')


    def FN6101(self):
        Type, Code, Name = self.GetParameter([1, 4, Core.Para_String])
        #Type: 1资产 2负债 3权益
        #Code: 账户类型/分账序号/账目序号
        #Name: 账户名称

        DB = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        if DB.Search({'Code': Code}, Count= True):
            return Bear.Result(-1, 'Account Already Exist')

        DB.Insert({
            'Code': str(Code),
            'Name': str(Name),
            'Type': str(Type),
            'Amount': float(0.00),
        })
        return Bear.Result(1, 'Account Create Success')

    def FN6102(self):
        Code, StartDate, EndDate, Amount, Label, Remark = self.GetParameter([4, Core.Para_Date, Core.Para_Date, Core.Para_Money, 4, Core.Para_String])
        #Code: 账户类型/分账序号/账目序号
        #StartDate: 发生时间
        #EndDate: 结束时间
        #Amount: 发生金额
        #Label: 账务类型
        #Remark: 备注
        #61021999..100.1001测试/

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] != '1':
            Amount = -Amount
        
        AccountAmount = float(AccountInfo[0]['Amount'])

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'StartDate': str(StartDate),
            'StartDateInt': int(StartDate[:-3]),
            'EndDate': str(EndDate),
            'EndDateInt': int(EndDate[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Remark': str(Remark),
        })
        BalanceSheet.Change({'Code': str(Code)},{
            '$set': {'Amount': AccountAmount + Amount}
        })
        return Bear.Result(1, 'Debit Record Success')

    def FN6103(self):
        Code, StartDate, EndDate, Amount, Label, Remark = self.GetParameter([4, Core.Para_Date, Core.Para_Date, Core.Para_Money, 4, Core.Para_String])
        #Code: 账户类型/分账序号/账目序号
        #StartDate: 发生时间
        #EndDate: 结束时间
        #Amount: 发生金额
        #Label: 账务类型
        #Remark: 备注
        #61031999..100.1001测试/

        BalanceSheet = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        AccountInfo = BalanceSheet.Search({'Code': str(Code)})
        if len(AccountInfo) == 0:
            return Bear.Result(-1, 'Account Does Not Exist')
        
        Amount = float(Amount)
        if AccountInfo[0]['Type'] == '1':
            Amount = -Amount

        AccountAmount = float(AccountInfo[0]['Amount'])

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Account.Insert({
            'StartDate': str(StartDate),
            'StartDateInt': int(StartDate[:-3]),
            'EndDate': str(EndDate),
            'EndDateInt': int(EndDate[:-3]),
            'Amount': float(Amount),
            'Label': str(Label),
            'Remark': str(Remark),
        })
        BalanceSheet.Change({'Code': str(Code)},{
            '$set': {'Amount': AccountAmount + Amount}
        })

        return Bear.Result(1, 'Credit Record Success')

    def FN6105(self):
        Code = self.GetParameter([4])
        #Code: 账户类型/分账序号/账目序号
        BalanceSheet  = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        if BalanceSheet.Search({'Code': Code}, Count= True) == 0:
            return Bear.Result(-1, 'Account Not Exist')

        DeletedAccountIndex = BalanceSheet.Search({'Code': Code})[0]
        if DeletedAccountIndex['Type'] == '1':
            if not BalanceSheet.Search({'Code': '6999'}, Count= True):
                BalanceSheet.Insert({
                    'Code': '6999',
                    'Name': '待处理资产账户',
                    'Type': '1',
                    'Amount': float(0.00),
                })  
            WaitingAccountIndex = BalanceSheet.Search({'Code': '6999'})[0]
            WaitingAccount = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account6999')

            Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code).DeleteTable()
            BalanceSheet.Delete({'Code': Code})
        elif DeletedAccountIndex['Type'] == '2':
            if not BalanceSheet.Search({'Code': '8999'}, Count= True):
                BalanceSheet.Insert({
                    'Code': '8999',
                    'Name': '待处理负债账户',
                    'Type': '2',
                    'Amount': float(0.00),
                })
            WaitingAccountIndex = BalanceSheet.Search({'Code': '8999'})[0]
            WaitingAccount = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account8999')

            Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code).DeleteTable()
            BalanceSheet.Delete({'Code': Code})
        else:
            if not BalanceSheet.Search({'Code': '9999'}, Count= True):
                BalanceSheet.Insert({
                    'Code': '9999',
                    'Name': '待处理权益账户',
                    'Type': '3',
                    'Amount': float(0.00),
                })
            WaitingAccountIndex = BalanceSheet.Search({'Code': '9999'})[0]
            WaitingAccount = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account9999')

            Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code).DeleteTable()
            BalanceSheet.Delete({'Code': Code})

        WaitingAccount.Insert({
            'StartDate': str(Cr.Date().String(-2)),
            'StartDateInt': int(Cr.Date().String(-2)[:-3]),
            'EndDate': str(Cr.Date().String(-2)),
            'EndDateInt': int(Cr.Date().String(-2)[:-3]),
            'Amount': float(DeletedAccountIndex['Amount']),
            'Label': str(9999),
            'Remark': '账户'+Code+'销记待处理',
        })
        BalanceSheet.Change({'Code': WaitingAccountIndex['Code']},{
            '$set': {'Amount': WaitingAccountIndex['Amount'] + DeletedAccountIndex['Amount']}
        })

        return Bear.Result(1, 'Account Delete Success')

    def FN6621(self):
        print('Success')


    def FN6606(self):
        Code, Start, End = self.GetParameter([4, Core.Para_Date, Core.Para_Date])
        #Code: 账户类型/分账序号/账目序号
        Start = int(Start[:-3])
        End = int(End[:-3])
        BalanceSheet  = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'BalanceSheet')

        if BalanceSheet.Search({'Code': Code}, Count= True) == 0:
            return Bear.Result(None, 'Account Not Exist')

        Account = Mongo.MongoDB('ConsoleServer', 'TimeCapsule', 'Account'+Code)
        Result = Account.Search({
            '$and': [
                {'StartDateInt': {'$gte': Start}},
                {'EndDateInt': {'$lte': End}},
            ]
        })
        Ret = []
        for Item in Result:
            Data = {}
            Data['Start'] = Item['StartDate']
            Data['End'] = Item['EndDate']
            Data['Amount'] = Item['Amount']
            Data['Label'] = Item['Label']
            Data['Remark'] = Item['Remark']
            Ret.append(Data)
        return Ret

    def FN6621(self):
        print('Success')


    def FN6901(self):
        print('Success')

    def FN6906(self):
        print('Success')

Core.NewModule(Account())
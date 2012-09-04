'''
Created on 15.11.2010

@author: Dennis.Erokhin
'''

class BankTrans():    
    '''
    Bank transaction record
    '''

    opDate = None
    checkDate = None
    opNum = None
    opPayee = None
    opCur = None
    opSum = None
    accSum = None
    trnType = None

    def __init__(self):
        '''
        Constructor
        '''
    
    def set_dates(self, opDate, checkDate, period):
        def replace_year(date):
            if date.month == period[0].month:
                date = date.replace(period[0].year)
            else:
                date = date.replace(period[1].year)
            return date
        
        if not checkDate:
            print("checkDate is None")
            checkDate = opDate

        self.opDate = replace_year(opDate)
        self.checkDate = replace_year(checkDate)
    
    def getTransRecord(self):
        return [self.opDate, self.checkDate, self.opNum, self.opPayee, self.opCur, self.opSum, self.accSum, self.trnType]
    
    def print_trans(self):
        print(self.opDate);
        print(self.checkDate);
        print(self.opNum);
        print(self.opPayee);
        print(self.opCur);
        print(self.opSum);
        print(self.accSum);
        print(self.trnType);
    
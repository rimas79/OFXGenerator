'''
Created on 15.11.2010

@author: Dennis.Erokhin
'''

from datetime import datetime

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
            assert len(date) == 5 or len(date) == 7
            date = date.lower()
            if len(date) == 5:
                date = date+str(period[0].year)[-2:]
            format = "%d%b%y"
#            print(date)
#            print(format)
            dt = datetime.strptime(date.encode("cp1251"), format)

            if dt.month == period[0].month:
                dt = dt.replace(period[0].year)
            else:
                dt = dt.replace(period[1].year)
            return dt
        
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
    
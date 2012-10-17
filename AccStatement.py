#-*- coding: cp1251 -*-
'''
Created on 28.09.2011

@author: Dennis.Erokhin
'''

class AccStatement():
    '''
    Statement holder
    '''
    __transList = None
    __acctID = None
    __FID = None
    __company = None
    __servDate = None
    __startDate = None
    __endDate = None

    def __init__(self):
        '''
        Constructor
        '''
        self.__transList = []

    def getTransHeader(self):
        return ["OpDate", "CheckDate", "OpNum", "OpPayee", "OpCur", "OpSum", "AccSum", "TrnType"]

    def get_trans_list(self):
        return self.__transList

    def insertTransaction(self, trans):
#TODO: если дата списания выбивается из периода отчета делать предупреждение
        if (trans.checkDate < self.__startDate or trans.checkDate > self.__endDate):
            print("date errors")
            print("start_date", self.__startDate)
            print("end_date", self.__endDate)
            print("op_date", trans.opDate)
            print("check_date", trans.checkDate)
            raise(Exception("Transaction check date error"))
        self.__transList.append(trans.getTransRecord())
#        self.__transList.append(trans)
    
    def __iter__(self):
        return iter(self.__transList)
#    
#    def next(self):
#        return self.next().getTransRecord();
    
    def get_acct_id(self):
        return self.__acctID

    def get_fid(self):
        return self.__FID

    def get_company(self):
        return self.__company

    def get_serv_date(self):
        return self.__servDate

    def get_start_date(self):
        return self.__startDate

    def get_end_date(self):
        return self.__endDate

    def getPeriod(self):
        return (self.__startDate, self.__endDate)

    def set_acct_id(self, value):
        self.__acctID = value

    def set_fid(self, value):
        self.__FID = value

    def set_company(self, value):
        self.__company = value

    def set_serv_date(self, value):
        self.__servDate = value

    def set_start_date(self, value):
        self.__startDate = value

    def set_end_date(self, value):
        self.__endDate = value

    def setCompany(self, company):
        self.__company = company
        
    def setFID(self, FID):
        self.__FID = FID


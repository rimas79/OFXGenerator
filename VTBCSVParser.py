#-*- coding: iso-8859-15 -*-
'''
Created on 19.11.2010

@author: Dennis.Erokhin
'''
from report_parser import ReportParser
import csv
import re
from datetime import datetime
from BankTrans import BankTrans

class VTBCSVParser(ReportParser):
    '''
    Parsing VTB csv files
    '''
    stCard = "CARD"
    stAcct = "ACCT"

    __file = None
    __writer = None
    __stmtReader = None
    __state = None
    __trans = None
    __prog = None

    def __init__(self, file, writer):
        '''
        Constructor
        '''
        self.__file = file
        self.__writer = writer
        self.__stmtReader = csv.reader(file, delimiter = ";")
        self.__prog = re.compile("(.*?)\s*(\d{6})")
        pass

    def parseReason(self, text):
        result = self.__prog.match(text)
        if result:
            return (result.group(1), result.group(2))

    def formatDate(self, text):
        dt = datetime.strptime(text, "%d.%m.%Y")
        return dt.strftime("%Y%m%d")
        pass        
        
    def formatDateEx(self, text):
        dt = datetime.strptime(text, "%d.%m.%Y %H:%M:%S")
        return dt.strftime("%Y%m%d")
        pass        
    
    def processCardRecord(self, row):
        self.__trans.opDate = self.formatDateEx(row[1])
        self.__trans.checkDate = self.formatDate(row[2])
        self.__trans.opSum = row[3]
        self.__trans.opCur = row[4]
        self.__trans.accSum = row[6]
        (payee, num) = self.parseReason(row[7])
        self.__trans.opPayee = payee
        self.__trans.opNum = num
        pass

    def processAccountRecord(self, row):
        print(",".join(row))
        self.__trans.opDate = self.formatDateEx(row[0])
        self.__trans.checkDate = self.__trans.opDate
        self.__trans.opNum = row[1]
        self.__trans.opSum = row[2]
        self.__trans.accSum = self.__trans.opSum
        self.__trans.opPayee = row[3]        
        pass
        
    def processRow(self, row):
        if self.__state == self.stCard:
            self.__trans = BankTrans()
            self.__trans.trnType = "CREDIT"
            self.processCardRecord(row)
            self.__writer.write(self.__trans)
        elif self.__state == self.stAcct:
            self.__trans = BankTrans()
            self.__trans.trnType = "DEP"
            self.processAccountRecord(row)
            self.__writer.write(self.__trans)
        if row[0] == "Номер счета":
            self.__writer.setAcctID(row[1])
        elif row[0] == "Номер карты":
            self.__state = self.stCard
        elif row[0] == "Дата":
            self.__state = self.stAcct
    
    def feed(self, text):        
        for row in self.__stmtReader:
#            print(",".join(row))
            self.processRow(row) 
        pass
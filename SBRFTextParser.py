#-*- coding: cp1251 -*-
'''
Created on 18.11.2010

@author: Dennis.Erokhin
'''
from report_parser import ReportParser, isCredit, format_trn_date
from BankTrans import BankTrans
import re

#const
_long_date_fmt = "\d\d\w{3}\d\d"
_head_rx = re.compile('ОТЧЕТ СОСТАВЛЕН ЗА ПЕРИОД.*')
_delim_str = re.compile('-[+]-')
_delim_rx = re.compile('[+]-*')
prog = re.compile(".*\s(\d\d\w{3})\s+(\d\d\w{3}\d\d)\s+.*\s+(\d+[.]\d{2}).*", re.LOCALE)
trans = re.compile(".*\s(\d\d\w{3})\s(\d\d\w{3}\d\d)\s([\dE+]{6})\s+(.{22})\s+(\w{0,3})\s+(\d*[.]*\d{0,2})\s+(\d+[.]\d{2}[CR]*).*", re.LOCALE)       

class SBRFTextParser(ReportParser):
    '''
    Parsing SBRF text repors
    '''
    _state = None

    def __init__(self, file, holder):
        '''
        initialization
        '''
        self.__statement = holder
        self.__file = file

    def get_next_line(self):
        line = self.__file.readline()
        return line
    
    def is_header(self, str):
        return str != "" and _head_rx.match(str)
    
    def is_delim(self, str):
        return str != "" and _delim_str.search(str)
     
    def get_statement_params(self, str):
        rx = '.*\s('+_long_date_fmt+')\s*-\s*('+_long_date_fmt+')\s*('+_long_date_fmt+').*'
        params_rx = re.compile(rx, re.L)
        result = params_rx.match(str)
        if result:
            print(result.groups())
            self.__statement.set_start_date(format_trn_date(result.group(1)))
            self.__statement.set_end_date(format_trn_date(result.group(2)))
            self.__statement.set_serv_date(format_trn_date(result.group(3)))  
        else:
            raise(Exception("non-header string in header position"))  
        
    def process_header(self):
        if self._state == 'begin':
            self._state = 'header'
            str = self.get_next_line()
            self.get_statement_params(str)
        
    def process_delim(self, str):
        delims = _delim_rx.finditer(str)
        if self._state == 'header':
            self._state = 'first_delim'
        elif self._state == 'first_delim':
            self._state = 'second_delim'
            self.pl_pos = [pl.start() for pl in delims]
        elif self._state == 'second_delim':
            self._state = 'third_delim'
        elif self._state == 'third_delim':
            self._state = 'first_delim'
    
    def process_trans(self, str):
        result = prog.match(str)        
        if result:
            fields = trans.match(str)
            assert fields
            print(fields.groups())
            curTrans = BankTrans()
            curTrans.trnType = "CREDIT"
            curTrans.set_dates(opDate = format_trn_date(fields.group(1)), \
                               checkDate = format_trn_date(fields.group(2)), \
                               period = self.__statement.getPeriod())
            curTrans.opNum = fields.group(3)
            curTrans.opPayee = fields.group(4).decode('cp1251')
            curTrans.opCur = fields.group(5)
            curTrans.opSum = fields.group(6)
            curTrans.accSum = isCredit(fields.group(7))
            self.__statement.insertTransaction(curTrans)
        pass
       
    def feed(self):
        self._state = 'begin'
        str = self.get_next_line()
        while str:
            if self.is_header(str):
                self.process_header()
            elif self.is_delim(str):
                self.process_delim(str)
            elif self._state == 'second_delim':
                self.process_trans(str)
            str = self.get_next_line()

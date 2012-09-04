#-*- coding: cp1251 -*-
'''
Created on 19.11.2010

@author: Dennis.Erokhin
'''
from datetime import datetime

def isCredit(sum):
    if sum.endswith("CR"):
        sum = sum.replace("CR","")
    else:
        sum = "-"+sum
    return str(sum)
    
def format_trn_date(date):
    assert len(date) == 5 or len(date) == 7
    date = date.lower()
    if len(date) == 5:
        format = "%d%b"
    elif len(date) == 7:
        format = "%d%b%y"
#    print(date)
#    print(format)
    dt = datetime.strptime(date.encode("cp1251"), format)
    return dt
    pass

class ReportParser():
    '''
    Parent class for all parsers
    '''

    __statement = None
    __file = None
    
    def __init__(self, file, holder):
        self.__statement = holder
        self.__file = file
        
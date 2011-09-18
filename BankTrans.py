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

    def __init__(self):
        '''
        Constructor
        '''
        
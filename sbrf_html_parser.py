'''
Created on 13.11.2010

@author: Dennis.Erokhin
'''
from report_parser import ReportParser, isCredit, format_trn_date
from BankTrans import BankTrans
import lxml.html

ROW_COUNT = 8; 

def debug_print(text):
    debug = 0;
    if debug > 0:
        print(text)
    
class SBRFHtmlParser(ReportParser):
    '''
    Parse SBRF CC report
    '''
    xpathAcctID="body/table[1]/tr[2]/td[1]/table[1]/tr[2]/td[1]"
    xpathServDate = "body/table/tr[2]/td[3]/table[1]/tr[2]/td";
    xpathRepPeriod = "body/table/tr[2]/td[3]/table[1]/tr[2]/td[2]/text()";

    def __init__(self, file, holder):
        self.__statement = holder
        self.__file = file

    def feed(self):
        doc = lxml.html.parse(self.__file)
        root = doc.getroot()
        txt1 = root.xpath(self.xpathAcctID)
        self.__statement.set_acct_id(txt1[0].text)
        
        txt1 = root.xpath(self.xpathServDate)
        debug_print(txt1)
        self.__statement.set_serv_date(format_trn_date(txt1[0].text))
        self.__statement.set_start_date(format_trn_date(txt1[1].text[0:7]))
        self.__statement.set_end_date(format_trn_date(txt1[1].text[-7:]))
        
        txt2 = root.xpath('body/table[2]/tr[@class="rowTrnData"]')
        for tr in txt2:
            curTrans = BankTrans()
            curTrans.trnType = "CREDIT"
            curTrans.set_dates(opDate = tr[1].text, \
                               checkDate = tr[2].text, \
                               period = self.__statement.getPeriod())
            curTrans.opNum = tr[3].text
            curTrans.opPayee = tr[4].text
            curTrans.opCur = tr[5].text
            if tr[6].text:
                curTrans.opSum = isCredit(tr[6].text)
            curTrans.accSum = isCredit(tr[7].text)
            self.__statement.insertTransaction(curTrans)

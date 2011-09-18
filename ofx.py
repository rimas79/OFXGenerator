'''
Created on 15.11.2010

@author: Dennis.Erokhin
'''

import xml.dom.minidom
import datetime
from OFXWriter import OFXWriter

class OFX(OFXWriter):
    '''
    Generate OFX document
    '''
    __doc= None
    __ofx = None
    __transList = None

    def __init__(self, file):
        OFXWriter.__init__(self, file)
        self.__doc = xml.dom.minidom.Document()
        self.__ofx = self.__doc.createElementNS("http://www.boddie.org.uk/paul/business", "OFX")
        self.__doc.appendChild(self.__ofx)        
        
    def addNode(self, parent, tagName, value = None):
        tag = self.__doc.createElement(tagName)
        parent.appendChild(tag)
        if (value):
            text = self.__doc.createTextNode(value)
            tag.appendChild(text)
        return tag
            
    def generateDocument(self):
# Sign on
        signon = self.addNode(self.__ofx, "SIGNONMSGSRSV1")
        sonrs = self.addNode(signon, "SONRS")        
        stat = self.addNode(sonrs, "STATUS")
        self.addNode(stat, "CODE", "0")
        self.addNode(stat, "SEVERITY", "INFO")
        dt = datetime.datetime.today()
        self.addNode(sonrs, "DTSERVER", dt.strftime("%Y%m%d%H%M%S"))
        self.addNode(sonrs, "LANGUAGE", "RUS")
        self.addNode(sonrs, "DTPROFUP", "20100501000000")
        self.addNode(sonrs, "DTACCTUP", dt.strftime("%Y%m%d%H%M%S"))
        fi = self.addNode(sonrs, "FI")
        self.addNode(fi, "ORG", "SBRF")
        self.addNode(fi, "FID", "1001") 
# Bank messages
        bankMsg = self.addNode(self.__ofx, "BANKMSGSRSV1")
        transResp = self.addNode(bankMsg, "STMTTRNRS")
        self.addNode(transResp, "TRNUID", "1001")
        stat = self.addNode(transResp, "STATUS")
        self.addNode(stat, "CODE", "0")
        self.addNode(stat, "SEVERITY", "INFO")
        stmtResp = self.addNode(transResp, "STMTRS")
        self.addNode(stmtResp, "CURDEF", "RUR")
        acct = self.addNode(stmtResp, "BANKACCTFROM")
        self.addNode(acct, "BANKID", "121099999")
        self.addNode(acct, "ACCTID", "999988")
        self.addNode(acct, "ACCTTYPE", "CHECKING")
        self.__transList = self.addNode(stmtResp, "BANKTRANLIST")
        self.addNode(self.__transList, "DTSTART", "20051001")
        self.addNode(self.__transList, "DTEND", "20051028")
        ledgBal = self.addNode(stmtResp, "LEDGERBAL")
        self.addNode(ledgBal, "BALAMT", "200.29")
        self.addNode(ledgBal, "DTASOF", "200510291120")
        avail = self.addNode(stmtResp, "AVAILBAL")
        self.addNode(avail, "BALAMT", "200.29")
        self.addNode(avail, "DTASOF", "200510291120")        

    def addTransaction(self, trans):
        stmtTrans = self.addNode(self.__transList, "STMTTRN")
        self.addNode(stmtTrans, "TRNTYPE", "CHECK")
        self.addNode(stmtTrans, "DTPOSTED", trans.opDate)
        self.addNode(stmtTrans, "DTUSER", trans.checkDate)        
        self.addNode(stmtTrans, "TRNAMT", trans.accSum)
        self.addNode(stmtTrans, "FITID", trans.opDate+trans.opNum)
        self.addNode(stmtTrans, "CHECKNUM", trans.opNum)

    def write(self, trans):
        self.addTransaction(trans)

    def printDocument(self):
        self.file_object.write(self.__doc.toprettyxml())
        
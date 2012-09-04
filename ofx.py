#-*- coding: cp1251 -*-
'''
Created on 15.11.2010

@author: Dennis.Erokhin
'''

from OFXWriter import OFXWriter
from lxml import etree as ET
from lxml.builder import E

class OFX(OFXWriter):
    '''
    Generate OFX document
    '''

    def __init__(self, file):
        OFXWriter.__init__(self, file)

    def saveFile(self, report):
        ofxDoc = (
            E.OFX(
                E.SIGNONMSGSRSV1(
                    E.SONRS(
                        E.STATUS(
                            E.CODE("0"),
                            E.SEVERITY("INFO")
                        ),
                        E.DTSERVER(report.get_serv_date().strftime("%Y%m%d")),
                        E.LANGUAGE("RUS"),
                        E.FI(
                           E.ORG(report.get_company()),
                           E.FID(report.get_fid())
                        )
                    )
                ),
                E.BANKMSGSRSV1(
                    E.STMTTRNRS(
                        E.TRNUID("1001")
                    ),
                    E.STATUS(
                        E.CODE("0"),
                        E.SEVERITY("INFO")
                    ),
                    E.STMTRS(
                        E.CURDEF("RUR"),
                        E.CCACCTFROM(
                            E.ACCTID(report.get_acct_id())
                        ),
                        E.BANKTRANLIST(
                            E.DTSTART(report.get_start_date().strftime("%Y%m%d")),
                            E.DTEND(report.get_end_date().strftime("%Y%m%d")),
                        )
                    )
                )
            )
        )
        
        transList = ofxDoc.find(".//BANKTRANLIST")
        for trans in report.get_trans_list():
            trns = (
                E.STMTTRN(
                    E.DTPOSTED(trans[0].strftime("%Y%m%d")), #.opDates
                    E.DTUSER(trans[1].strftime("%Y%m%d")), #.checkDate
                    E.TRNAMT(trans[6]), #.accSum
                    E.FITID(str(trans[0].strftime("%Y%m%d")) + str(trans[2])), #.opDate, .opNum
                    E.CHECKNUM(trans[2]), #.opNum
                    E.NAME(trans[3]), #.opPayee
                    E.MEMO(trans[3]) #.opPayee
                )
            )
            transList.append(trns)
#        print(ET.tostring(ofxDoc, pretty_print=True))
        self.file_object.write(ET.tostring(ofxDoc, pretty_print=True))
        
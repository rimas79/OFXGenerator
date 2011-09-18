'''
Created on 13.11.2010

@author: Dennis.Erokhin
'''
from html.parser import HTMLParser
from datetime import datetime
import BankTrans

ROW_COUNT = 8; 

class SbrfHtmlParser(HTMLParser):
    '''
    Parse SBRF CC report
    '''
    
    state = 0;
    data_row_num = 0;
    writer = None
    curTrans = None

    def __init__(self, writer):
        HTMLParser.__init__(self)
        self.writer = writer
        self.curTrans = BankTrans

    def debug_print(self, text):
        debug = 0;
        if debug > 0:
            print(text)
    
    def format_date(self, date):
        dt = datetime.strptime(date, "%d%b")
        self.debug_print(dt.strftime("%d.%m.%Y"))
        dt = dt.replace(2010)
        return dt.strftime("%d.%m.%Y")
        pass
    
    def handle_starttag(self, tag, attrs):
        if self.state == 0 and \
            tag == "tr" and \
            len(attrs) > 0 and\
            attrs[0][1] == "rowTrnData":
            self.debug_print("Start!")
            self.state = 1
        if self.state == 1 and \
            tag == "td":
            self.state = 2
            self.data_row_num += 1
                
    def handle_data(self, data):
        if self.state == 2:
#            self.debug_print(self.data_row_num,":",data)
#            self.debug_print("pos:",self.getpos()[0],self.getpos()[1])
            cur_row_num = self.data_row_num % ROW_COUNT
            if cur_row_num == 1:
#                self.cur_record[cur_row_num - 1] += data
                pass
            elif cur_row_num == 2:
                self.curTrans.opDate = self.format_date(data)
            elif cur_row_num == 3:
                self.curTrans.checkDate = self.format_date(data)
            elif cur_row_num == 4:
                self.curTrans.opNum = data
            elif cur_row_num == 5:
                self.curTrans.opPayee = data
            elif cur_row_num == 6:
                self.curTrans.opCur = data
            elif cur_row_num == 7:
                self.curTrans.opSum = data
            elif cur_row_num == 0:
                self.curTrans.accSum = data

    def handle_endtag(self, tag):
        if self.state == 1 and \
            tag == "tr":
            self.debug_print("Stop!")
            self.state = 0
            self.data_row_num = 0
            self.writer.write(self.curTrans)
            self.curTrans = BankTrans
        if self.state == 2 and\
            tag == "td":
            self.state = 1
            
    def print_records(self):
        [print(x) for x in self.records];
#-*- coding: cp1251 -*-
'''
Created on 13.11.2010

@author: Dennis.Erokhin
'''
from SBRFTextParser import SBRFTextParser
from sbrf_html_parser import SBRFHtmlParser
from VTBCSVParser import VTBCSVParser
from ofx import OFX
import csv
from AccStatement import AccStatement
import locale
import codecs
import cStringIO
from os.path import splitext
import argparse

VTB = "VTB"
SBRFT = "SBRFT"
SBRFH = "SBRFH"

locale.setlocale(locale.LC_ALL, 'russian')

fileType = None
    
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        res = [];
        for s in row:
            if hasattr(s, 'encode'):
                res.append(s.encode("utf-8"))
            else:
                res.append(s)
#        self.writer.writerow([s.encode("utf-8") for s in row if type(s)!='datetime.datetime'])
        self.writer.writerow(res)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)    

def fileProcess(inFileName, fileType, outFileName, outFileType):
    print(inFileName)
    
    fileName= splitext(inFileName)[0].lower()
#    
#    fileExt = splitext(name)[1].lower()
#    
#    if fileExt == ".csv":
#        fileType = VTB
#    elif fileExt == ".txt":
#        fileType = SBRFT
#    elif fileExt == ".html":
#        fileType = SBRFH
#    else:
#        raise NotImplementedError()
#        
    rep = AccStatement()
    print(fileType)
    with open(inFileName, 'r') as f:        
        if fileType == VTB:
            myParser = VTBCSVParser(f, rep)
        elif fileType == SBRFT:
            rep.set_acct_id(fileName[0:4])
            myParser = SBRFTextParser(f, rep)
        elif fileType == SBRFH:
            myParser = SBRFHtmlParser(f, rep)                       
        else:
            raise NotImplementedError()        
        rep.setCompany(fileType)
        rep.setFID("1001")
        myParser.feed()
    f.close()
    
    print(outFileType)
    print(rep)
    if outFileType == "OFX":
        with open(outFileName, "w") as file_object:
            myOFX = OFX(file_object)
            myOFX.saveFile(rep)
    elif  outFileType == "CSV":
        myCsv = UnicodeWriter(open(outFileName, 'w'), dialect='excel', lineterminator='\n', delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        myCsv.writerow(rep.getTransHeader())
        myCsv.writerows(rep)
    else:
        raise NotImplementedError()      
        file_object.closed
    rep = None   

if __name__ == '__main__':
    print("Hello, World!")

'''
for root, dirs, files in os.walk("../IN/"):
    for name in files:
        fileName = join(root, name) 
        fileProcess(root, name)
'''
parser = argparse.ArgumentParser(description='Convert bank reports')
parser.add_argument('-i', '--input', help='input file type', choices=['VTB', 'SBRFT', 'SBRFH'])
parser.add_argument('-o', '--output', help='output file type', choices=['OFX', 'CSV'])
parser.add_argument('input_file', help='input file name')
parser.add_argument('output_file', help='output file name')


args = parser.parse_args()
print (args)
fileProcess(args.input_file, args.input, args.output_file, args.output)
        
exit()

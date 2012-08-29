#-*- coding: cp1251 -*-
'''
Created on 13.11.2010

@author: Dennis.Erokhin
'''
from SBRFTextParser import SBRFTextParser
from sbrf_html_parser import SBRFHtmlParser
from VTBCSVParser import VTBCSVParser
from ofx import OFX
from AccStatement import AccStatement
import locale
import os
from os.path import join, splitext

VTB = "VTB"
SBRFT = "SBRFT"
SBRFH = "SBRFH"

locale.setlocale(locale.LC_ALL, 'russian')

fileType = None
    
def fileProcess(root, name):
    inFileName = join(root, name)
    print(inFileName)
    fileName= splitext(name)[0].lower()
    fileExt = splitext(name)[1].lower()
    if fileExt == ".csv":
        fileType = VTB
    elif fileExt == ".txt":
        fileType = SBRFT
    elif fileExt == ".html":
        fileType = SBRFH
    else:
        raise NotImplementedError()
    print(fileType)

    rep = AccStatement()
    print(rep)
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
    
    outFileName = "../OUT/"+name+".ofx"
    with open(outFileName, "w") as file_object:
        myOFX = OFX(file_object)
        myOFX.saveFile(rep)        
#        shutil.move(inFileName, "../ARC/")
        file_object.closed
    rep = None   

if __name__ == '__main__':
    print("Hello, World!")

for root, dirs, files in os.walk("../IN/"):
    for name in files:
        fileName = join(root, name) 
        fileProcess(root, name)
exit()

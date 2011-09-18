'''
Created on 13.11.2010

@author: Dennis.Erokhin
'''
from sbrf_html_parser import SbrfHtmlParser
from ofx import OFX
import locale
locale.setlocale(locale.LC_ALL, 'russian')

if __name__ == '__main__':
    print("Hello, World!")

with open('../OUT/qwe.ofx', "w") as file_object:
    myofx = OFX(file_object)
    myofx.generateDocument()
    myparser = SbrfHtmlParser(myofx)    
    with open('../IN/7394_Oct10.html', 'r') as f:
        read_data = f.read()
        myparser.feed(read_data)
    f.closed
#    myparser.print_records()

    myofx.printDocument()
file_object.closed
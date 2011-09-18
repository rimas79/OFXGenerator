'''
Created on 15.11.2010

@author: Dennis.Erokhin
'''

class OFXWriter():
    '''
    Write OFX to FILE
    '''
    file_object = None;

    def __init__(self, file):
        '''
        Constructor
        '''
        self.file_object = file;
        
    def write(self):
        pass
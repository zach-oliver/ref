# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/26/17
@author: Zachary Oliver
"""

from os_functions import create_Folders_Along_Path, get_Current_Date_Time

class Log:
    
    def __init__(self, filename='', function='', prefix='', log_dir='', separator='|:|', DEBUG=False):
        if prefix != '':
            print "log.py WARNING: %s prefix will no longer be used. Switch to filename instead for better logging." % (prefix)
        self.loc = get_Current_Date_Time(AS_STR=True) + filename + '.log'
        self.DEBUG = DEBUG
        if self.DEBUG:
            print "log.py --> Log --> self.loc (file name): %s" % self.loc
        
        self.loc = "%s%s" % (log_dir, self.loc)

        if self.DEBUG:
            print "log.py --> Log --> self.loc (full path): %s" % self.loc
            
        self.FILENAME = filename
        
        self.write(self.FILENAME)
        
        self.FUNCTION = function
        self.SEPARATOR = separator
    
    # can be deprecated as append will create file if it doesn't exist
    def write(self, log_line):
        create_Folders_Along_Path(self.loc)
        
        with open(self.loc, "a") as f:
            f.write(log_line)
            f.write("\n")
    
    # adds log_line to the end of the file
    # doesn't handle non-strings
    def append(self, str_log_line):
        create_Folders_Along_Path(self.loc)
        
        log_line = str(self.FUNCTION) + str(self.SEPARATOR) + str(str_log_line)
        
        if self.DEBUG:
            print log_line
        with open(self.loc, "a") as f:
            f.write(log_line)
            f.write("\n")

    def change_log_details(self, str_filename, str_function):
        self.FILENAME = str_filename
        self.FUNCTION = str_function

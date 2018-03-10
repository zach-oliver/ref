# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/26/17
@author: Zachary Oliver
"""

import datetime
import os
import errno

DEBUG = False

class Log:
    
    def __init__(self, prefix='', log_dir=''):
        #self.loc = LOG_DIR + str(datetime.datetime.now()) + prefix + '.txt'
        self.loc = str(datetime.datetime.now()) + '/' + prefix + '_' + str(datetime.datetime.now()) + '.txt'
        if DEBUG:
            print "log.py --> Log --> self.loc (file name): %s" % self.loc
        
        # use the below if you need cwd
        '''
        cwd = get_Current_Working_Directory()
        if DEBUG:
            print "log.py --> Log --> cwd (full path): %s" % str(cwd)
        self.loc = "%s%s%s" % (cwd, log_dir, self.loc)
        '''
        
        self.loc = "%s%s" % (log_dir, self.loc)

        if DEBUG:
            print "log.py --> Log --> self.loc (full path): %s" % self.loc
        
        # windows
        '''
        temp = os.path.join('.', LOG_DIR)
        print 'temp: ' + temp
        #self.loc = os.path.relpath(os.path.join(temp, self.loc))
        self.loc = os.path.join(temp, self.loc)
        self.loc = str(self.loc).replace(':','-')
        self.loc = str(self.loc).replace(' ','_')
        
        self.loc = LOG_DIR + str(datetime.datetime.now()) + prefix + '.txt'
        self.loc = os.path.relpath(os.path.join(LOG_DIR, self.loc))
        self.loc = str(self.loc).replace(':','-')
        self.loc = str(self.loc).replace(' ','_')
        print self.loc
        '''
    
    # can be deprecated as append will create file if it doesn't exist
    def write(self, log_line):
        with open(self.loc, "w") as f:
            f.write(log_line)
            f.write("\n")
    
    # adds log_line to the end of the file
    # doesn't handle non-strings
    def append(self, log_line):
        # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
        # creates the directory and any parent directories if it doesn't exist
        if not os.path.exists(os.path.dirname(self.loc)):
            try:
                os.makedirs(os.path.dirname(self.loc))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(self.loc, "a") as f:
            f.write(log_line)
            f.write("\n")

# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/26/17
@author: Zachary Oliver
"""

import datetime

DEBUG = False

class Log:
    
    def __init__(self, prefix='', log_dir=''):
        #self.loc = LOG_DIR + str(datetime.datetime.now()) + prefix + '.txt'
        self.loc = prefix + '_' + str(datetime.datetime.now()) + '.txt'
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

    def write(self, log_line):
        with open(self.loc, "w") as f:
            f.write(log_line)
            f.write("\n")
    
    # adds log_line to the end of the file
    # doesn't handle non-strings
    def append(self, log_line):
        with open(self.loc, "a") as f:
            f.write(log_line)
            f.write("\n")

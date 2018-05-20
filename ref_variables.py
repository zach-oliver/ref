# -*- coding: utf-8 -*-
#!/usr/bin/env python2
"""
Created on 5/13/18
@author: Zachary Oliver
"""
from os_functions import get_Current_Working_Directory

DEBUG = False

# get full path based on current working directory instead of relative
cwd = get_Current_Working_Directory()
if DEBUG:
    print "project_directories.py --> cwd (Full directory): %s" % cwd

#iOS VERSION BELOW - doesn't like leading '/' in front of folder name

LOG_DIR = r"%s/log/" % cwd
if DEBUG:
    print "project_directories.py --> LOG_DIR (Full directory): %s" % LOG_DIR

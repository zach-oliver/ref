# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/28/17
@author: Zachary Oliver
"""

import os, shutil
import errno
import datetime

DEBUG = True

# https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
def delete_All_In_Folder(folder):
    #folder = '/path/to/folder'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print "os_functions.py --> delete_All_In_Folder --> " + str(unicode(e))

def delete_All_Not_Subfolders(folder):
    #folder = '/path/to/folder'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print "os_functions.py --> delete_All_In_Folder --> " + str(unicode(e))

# deletes all files within a folder and within its subfolders            
def delete_Files_Not_Folders(folder, log):     
    os.chdir(folder)
    for root, dirs, files in os.walk(".", topdown = False):
       for file in files:
           if DEBUG:
               print(os.path.join(root, file))
           log.append(str(os.path.join(root, file)))
           os.remove(os.path.join(root, file))

def delete_File(filename, log):
    if DEBUG:
        print(filename)
    log.append(filename)
    os.remove(filename)

#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def get_Current_Working_Directory():
    return str(os.getcwd())

def create_Folders_Along_Path(path):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    # creates the directory and any parent directories if it doesn't exist
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
                
def get_Current_Date():
    return datetime.datetime.now().date().strftime('%Y-%m-%d')

# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
def get_Current_Date_Minus_Days(days_to_subtract):
    return (datetime.datetime.now().date() - datetime.timedelta(days=days_to_subtract)).strftime('%Y-%m-%d')

def get_Mod_Date_Time(filename):
    return os.path.getmtime(filename)

def get_Mod_Date(filename):
    return datetime.datetime.fromtimestamp(get_Mod_Date_Time(filename)).strftime('%Y-%m-%d')

def evaluate_Mod_Date(filename, minus_days):
    return (get_Mod_Date(filename) < get_Current_Date_Minus_Days(minus_days))

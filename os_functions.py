# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/28/17
@author: Zachary Oliver
"""

import os, shutil
import errno
import datetime
import glob

DEBUG = False

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
           path = os.path.join(root, file)
           if DEBUG:
               print(path)
           log.append(str(path))
           # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
           if os.path.exists(path):
               os.remove(path)
           else:
               msg = "delete_File_Not_Folders --> %s: file not found" % path
               print msg
               log.append(msg)

def delete_File(filename, log):
    if DEBUG:
        print(filename)
    log.append(filename)
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if os.path.exists(filename):
        os.remove(filename)
    else:
        msg = "delete_File --> %s: file not found" % filename
        print msg
        log.append(msg)

def create_Folders_Along_Path(path):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    # creates the directory and any parent directories if it doesn't exist
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def get_Current_Working_Directory():
    return str(os.getcwd())

def get_Current_Date():
    return datetime.datetime.now().date().strftime('%Y-%m-%d')

def get_Current_Date_Time():
    return datetime.datetime.now()

# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
def get_Current_Date_Minus_Days(days_to_subtract):
    return (datetime.datetime.now().date() - datetime.timedelta(days=days_to_subtract)).strftime('%Y-%m-%d')

def get_Mod_Date_Time(filename):
    if evaluate_If_File_Exists(filename):
        return os.path.getmtime(filename)
    else:
        return 0

def get_Mod_Date(filename):
    return datetime.datetime.fromtimestamp(get_Mod_Date_Time(filename)).strftime('%Y-%m-%d')

def get_File_List(filename):
    # example value ('~/folder1/folder2' + '*.png') # * means all. If need specific format then *.csv
    return glob.glob(filename)

def evaluate_Mod_Date(filename, minus_days):
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if evaluate_If_File_Exists(filename):
        # if the mod date of filename is older than today - minus days return True so you know to perform action
        # if not, false so don't perform an action
        return (get_Mod_Date(filename) < get_Current_Date_Minus_Days(minus_days))
    else:
        # file not found so perform action
        return True

def evaluate_If_File_Exists(filename):
    return os.path.isfile(filename)

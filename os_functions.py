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
import imp

# https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
def delete_All_In_Folder(folder):
    #folder = '/path/to/folder'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif evaluate_If_Folder_Exists(file_path):
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
def delete_Files_Not_Folders(folder, log, DEBUG=False):
    cwd = get_Current_Working_Directory()
    if evaluate_If_Folder_Exists(folder):
        msg = "delete_File_Not_Folders --> %s: Folder EXISTS" % folder
        if DEBUG:
            print msg
        log.append(msg)
        os.chdir(folder)
        for root, dirs, files in os.walk(".", topdown = False):
           for file in files:
               path = os.path.join(root, file)
               msg = "delete_File_Not_Folders --> %s FILE FOUND" % path
               if DEBUG:
                   print(path)
               log.append(str(path))
               # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
               if os.path.exists(path):
                   msg = "delete_File_Not_Folders --> %s EXISTS" % path
                   if DEBUG:
                       print(path)
                   log.append(msg)
                   #os.remove(os.path.join(path, file))
                   os.remove(path)
               else:
                   msg = "delete_File_Not_Folders --> %s: file not found" % path
                   print msg
                   log.append(msg)
        # change the folder back to the original CWD after crawling the folder
        os.chdir(cwd)
    else:
        msg = "delete_File_Not_Folders --> %s: folder not found" % folder
        print msg
        log.append(msg)

def delete_File(filename, log, DEBUG=False):
    if DEBUG:
        print(filename)
    log.append(filename)
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if os.path.exists(filename):
        os.remove(filename)
    else:
        msg = "delete_File --> %s: file not found" % filename
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

def get_Mod_Date_Time(filename, log):
    if evaluate_If_File_Exists(filename):
        return os.path.getmtime(filename)
    else:
        return 0

def get_Mod_Date(filename, log):
    return datetime.datetime.fromtimestamp(get_Mod_Date_Time(filename, log)).strftime('%Y-%m-%d')

def get_File_List(filename):
    # example value ('~/folder1/folder2' + '*.png') # * means all. If need specific format then *.csv
    return glob.glob(filename)

# https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-from-python
def get_Environment_Variable(str_env_var):
    return os.environ.get(str_env_var)

# https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-from-python
def get_Environment_Variable_or_Default(str_env_var, default_value):
    return os.getenv(str_env_var, default_value)

def evaluate_Mod_Date(filename, minus_days, log):
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if evaluate_If_File_Exists(filename):
        # if the mod date of filename is older than today - minus days return True so you know to perform action
        # if not, false so don't perform an action
        return (get_Mod_Date(filename, log) < get_Current_Date_Minus_Days(minus_days))
    else:
        # file not found so perform action
        return True

def evaluate_If_File_Exists(relative_filename, DEBUG=False):
    full_path = os.path.join(get_Current_Working_Directory(), relative_filename)
    if DEBUG:
        print "evaluate_If_File_Exists --> full_path: %s" % full_path
        print os.path.isfile(full_path)
    return os.path.isfile(full_path)

def evaluate_If_Folder_Exists(full_path, DEBUG=False):
    if DEBUG:
        print "evaluate_If_Folder_Exists --> full_path: %s" % full_path
        print os.path.isdir(full_path)
    return os.path.isdir(full_path)

# https://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it
def evaluate_If_Module_Exists(str_module):
    try:
        imp.find_module(str_module)
        return True
    except ImportError:
        return False

# https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python
def evaluate_Time_Difference(later_time, earlier_time, DEBUG=False):
    duration = later_time - earlier_time                         # For build-in functions
    duration_in_s = duration.total_seconds()
    days    = divmod(duration_in_s, 86400)        # Get days (without [0]!)
    hours   = divmod(days[1], 3600)               # Use remainder of days to calc hours
    minutes = divmod(hours[1], 60)                # Use remainder of hours to calc minutes
    seconds = divmod(minutes[1], 1)               # Use remainder of minutes to calc seconds
    microseconds = duration.microseconds
    time = "%d:%d:%d:%d.%d" % (days[0], hours[0], minutes[0], seconds[0], microseconds)
    if DEBUG:
        print time
    return time

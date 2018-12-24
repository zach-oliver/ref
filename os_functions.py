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
from dateutil.relativedelta import relativedelta

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

# UNIT TESTED
def delete_File(filename, DEBUG=False):
    if DEBUG:
        print(filename)
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if os.path.exists(filename):
        os.remove(filename)
    else:
        if DEBUG:
            print "delete_File --> %s: file not found" % filename

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

def join_With_Current_Working_Directory(str_local_dir):
    full_path = os.path.join(get_Current_Working_Directory(), str_local_dir)
    #return '%s%s' % (str(os.getcwd()), str_local_dir)
    return full_path

# UNIT TESTED
def get_Current_Date(AS_STR=False):
    if AS_STR:
        return datetime.datetime.now().date().strftime('%Y-%m-%d')
    else:
        return datetime.datetime.now().date()

# UNIT TESTED
def get_Current_Date_Time(AS_STR=False):
    if AS_STR:
        return str(datetime.datetime.now())
    else:
        return datetime.datetime.now()

# DEPRECATE!!!
def get_Current_Date_Time_As_Str():
    return str(datetime.datetime.now())

# https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date
def get_Current_Date_Minus_Days(int_days_to_subtract):
    return (datetime.datetime.now().date() - datetime.timedelta(days=int_days_to_subtract)).strftime('%Y-%m-%d')

# UNIT TESTED
def get_Current_Date_Minus_Months(int_months, AS_STR=False):
    if AS_STR:
        d = datetime.date.today() + relativedelta(months=-int_months)
        return d.strftime('%Y-%m-%d')
    else:
        return (datetime.date.today() + relativedelta(months=-int_months))

# UNIT TESTED
def get_Mod_Date_Time(filename):
    if evaluate_If_File_Exists(filename):
        return datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    else:
        return 0

def get_Mod_Date(filename):
    if evaluate_If_File_Exists(filename):
        return get_Mod_Date_Time(filename).strftime('%Y-%m-%d')
    else:
        return 0

def convert_Date_Time_To_Date(datetime_object):
    return datetime.datetime.fromtimestamp(datetime_object).strftime('%Y-%m-%d')

def convert_To_Date_Time(date_object):
    return datetime.datetime.strptime(datetime.datetime.strftime(date_object, '%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')

# UNIT TESTED
# LOCAL vs UTC ISSUE: https://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python/8778548#8778548
# Maybe update epoch instead?
def convert_Datetime_To_Timestamp(datetime_obj, epoch=datetime.datetime(1970,1,1)):
    # utc time = local time              - utc offset
    #utc_naive  = datetime_obj.replace(tzinfo=None) - datetime_obj.utcoffset()
    td = datetime_obj - epoch
    #return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
    return td.total_seconds()

def get_File_List(filename):
    # example value ('~/folder1/folder2' + '*.png') # * means all. If need specific format then *.csv
    return glob.glob(filename)

# https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python
def get_File_Size(str_filename):
    if evaluate_If_File_Exists(str_filename):
        return os.path.getsize(str_filename)
    else:
        return 0

# https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-from-python
def get_Environment_Variable(str_env_var):
    return os.environ.get(str_env_var)

# https://stackoverflow.com/questions/4906977/how-do-i-access-environment-variables-from-python
def get_Environment_Variable_or_Default(str_env_var, default_value):
    return os.getenv(str_env_var, default_value)

def evaluate_Mod_Date(str_filename, minus_days):
    # https://stackoverflow.com/questions/82831/how-to-check-whether-a-file-exists
    if evaluate_If_File_Exists(str_filename):
        # if the mod date of filename is older than today - minus days return True so you know to perform action
        # if not, false so don't perform an action
        return (get_Mod_Date(str_filename) < get_Current_Date_Minus_Days(minus_days))
    else:
        # file not found so perform action
        return True

# UNIT TESTED
# https://www.tutorialspoint.com/python/os_utime.htm
def change_Mod_Date(str_filename, datetime_object):
    os.utime(str_filename, (convert_Datetime_To_Timestamp(datetime_object), convert_Datetime_To_Timestamp(datetime_object)))

def evaluate_If_File_Exists(relative_filename, DEBUG=False):
    full_path = join_With_Current_Working_Directory(relative_filename)
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
    time_time = "%d:%d:%d:%d.%d" % (days[0], hours[0], minutes[0], seconds[0], microseconds)
    if DEBUG:
        print time_time
    return time_time

# https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file
def file_Line_Prepender(filename_str, line_str):
    with open(filename_str, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line_str.rstrip('\r\n') + '\n' + content)

# https://www.pythoncentral.io/how-to-rename-move-a-file-in-python/
def move_File(source_str, destination_str):
    shutil.move(source_str, destination_str)

# UNIT TESTED
def create_File(destination_str='temp.txt', test_str='test'):
    with open(destination_str, "a") as f:
        f.write(test_str)
        f.write("\n")

''' *******************************************************************
***************************     UNIT TESTING    ***********************
***********************************************************************
'''
def UNIT_TESTING(DEBUG=False):
    if DEBUG:
        this_file = 'os_functions.py'
        
        datetime_orig_last_modified = get_Mod_Date_Time(this_file)
        print "%s last modified date: %s" % (this_file, str(datetime_orig_last_modified))
        timestamp_orig_last_modified = convert_Datetime_To_Timestamp(datetime_orig_last_modified)
        print "%s last modified date in timestamp: %s" % (this_file, str(timestamp_orig_last_modified))
        
        temp_file = 'temp.txt'
        create_File(destination_str=temp_file)
        
        datetime_last_modified = get_Mod_Date_Time(temp_file)
        print "%s last modified date: %s" % (temp_file, str(datetime_last_modified))
        timestamp_last_modified = convert_Datetime_To_Timestamp(datetime_last_modified)
        print "%s last modified date in timestamp: %s" % (temp_file, str(timestamp_last_modified))
        
        args = {
            'str_filename': temp_file,
            'datetime_object': datetime_orig_last_modified
        }
        change_Mod_Date(**args)
        print "%s last modified date changed to: %s" % (temp_file, str(datetime_orig_last_modified))
        
        datetime_last_modified = get_Mod_Date_Time(temp_file)
        print "%s last modified date: %s" % (temp_file, str(datetime_last_modified))
        timestamp_last_modified = convert_Datetime_To_Timestamp(datetime_last_modified)
        print "%s last modified date in time: %s" % (temp_file, str(timestamp_last_modified))
        delete_File(temp_file)
        
        print get_Current_Date(AS_STR=True)
        print get_Current_Date_Minus_Months(3, AS_STR=True)
        print get_Current_Date_Time(AS_STR=True)

UNIT_TESTING()


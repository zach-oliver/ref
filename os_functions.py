# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 12/28/17
@author: Zachary Oliver
"""

import os, shutil

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
          print(os.path.join(root, file))
          log.append(str(os.path.join(root, file)))
          os.remove(os.path.join(root, file))

#https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
def get_Current_Working_Directory():
    return str(os.getcwd())
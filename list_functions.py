# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

'''********************************************
*********************PRINT*********************
***********************************************
'''
def list_print(list):
    for p in list: print p

'''********************************************
*********************SORT**********************
***********************************************
'''
def list_sort(list):
    list.sort()

'''********************************************
*********************FIND**********************
***********************************************
'''
def list_find_all(list, find):
    return [index for index, item in enumerate(list) if item == find]

'''********************************************
*********************REPLACE*******************
***********************************************
'''
def list_replace_all(list, original, new):
    for index, item in enumerate(list):
        if item == original:
            list[index] = new

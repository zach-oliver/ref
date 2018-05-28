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
*********************APPEND********************
***********************************************
'''
def list_append(list, value):
    list.append(value)

'''********************************************
*********************FIND**********************
***********************************************
'''
def list_find(list, find):
    return list.index(find)

def list_find_all(list, find):
    return [index for index, item in enumerate(list) if item == find]

def list_find_minimum_value_index(list):
    return list.index(min(list))

def list_find_maximum_value_index(list):
    return list.index(max(list))

'''********************************************
*********************REPLACE*******************
***********************************************
'''
def list_replace_all(list, original, new):
    for index, item in enumerate(list):
        if item == original:
            list[index] = new

'''********************************************
*********************REPLACE*******************
***********************************************
'''
def list_create_list_dict(keys):
    return {elem : [] for elem in keys}
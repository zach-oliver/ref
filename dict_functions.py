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
def dict_print_value(dict, value):
    print dict[value]

def dict_print_keys(dict):
    print dict[0].keys()

'''********************************************
*********************ADD***********************
***********************************************
'''
def dict_add_value(dict, key, value):
    dict[key] = value

'''********************************************
*********************CHANGE********************
***********************************************
'''
def dict_change_value(dict, key, value):
    dict_add_value(dict, key, value)

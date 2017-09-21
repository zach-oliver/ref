# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

def dict_print_value(dict, value):
    print dict[value]

def dict_add_value(dict, key, value):
    dict[key] = value

def dict_change_value(dict, key, value):
    dict_add_value(dict, key, value)

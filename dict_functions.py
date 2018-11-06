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
def dict_print_value(d, key):
    print d[key]

def dict_print_keys(d):
    print d[0].keys()

'''********************************************
*********************GET***********************
***********************************************
'''
def dict_get_value(d, key):
    return d[key]

def dict_get_value_or_default(d, key, default_value):
    return d.get(key, default_value)

'''********************************************
*********************ADD***********************
***********************************************
'''
def dict_add_value(d, key, value):
    d[key] = value

'''********************************************
*********************CHANGE********************
***********************************************
'''
def dict_change_value(d, key, value):
    dict_add_value(d, key, value)

'''********************************************
*********************CHANGE********************
***********************************************
'''
# https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
def dict_merge(dictx, dicty):
    dictz = dictx.copy()   # start with x's keys and values
    dictz.update(dicty)    # modifies z with y's keys and values & returns None
    return dictz
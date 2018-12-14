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

#https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
# UNIT TESTED
def dict_print_describe(d):
    for key, value in d.iteritems():
        print 'Key: %s' % str(key)
        print 'Value:'
        print value

'''********************************************
*********************OUTPUT********************
***********************************************
'''
#https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
# UNIT TESTED
def dict_output_describe_list(d):
    output = []
    if d is not None:
        for key, value in d.iteritems():
            output.append('Key: %s' % str(key))
            output.append('Value:')
            output.append(str(value))
    return output

'''********************************************
*********************SORT********************
***********************************************
'''
# UNIT TESTED
def dict_sort_by_value(d):
    return sorted(d.items(), key=lambda x: x[1])

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
*********************MERGE********************
***********************************************
'''
# realpython.com
def dict_merge(dictx, dicty):
    return dict(dictx, **dicty)

'''********************************************
*********************CREATE********************
***********************************************
'''
# UNIT TESTED
def dict_create_basic():
    return {'a': 1, 'b': 2, 'c': 3, 'd': 4}

'''********************************************
*********************SEARCH********************
***********************************************
'''
# https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
# UNIT TESTED
def dict_search_keys(d, key):
    return key in d


'''*******************************************************************
********************       UNIT TESTS      ***************************
**********************************************************************
'''
d = dict_create_basic()
if d is None:
    print 'dict_functions FAILED: dict_create_basic is None'
#dict_print_describe(d)

list_dict_sort = dict_sort_by_value(d)
if list_dict_sort[0][0] != 'a' or list_dict_sort[3][1] != 4:
    print 'dict_functions FAILED: dict_sort_by_value not correct'

list_dict_output = dict_output_describe_list(d)
if list_dict_output[0] != 'Key: a' or list_dict_output[5] != '3':
    print 'dict_functions FAILED: dict_output_describe_list not correct'

if not dict_search_keys(d, 'a') or dict_search_keys(d, 'e'):
    print 'dict_functions FALILED: dict_search_keys not correct'

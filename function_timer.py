# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/9/18
@author: Zachary Oliver
"""

# discovered by email from realpython.com
# https://docs.python.org/2/library/timeit.html#python-interface

# The "timeit" module lets you measure the execution
# time of small bits of Python code

import timeit
from fancy_python import create_function_variable_from_function_and_arguments

def time_my_function(function_to_time):
    #t = Timer(stmt='pass', setup='pass')       # outside the try/except
    t = timeit.Timer(stmt=function_to_time, setup='pass')
    try:
        float_seconds = t.timeit(number=1)    # or t.repeat(...)
        return float_seconds
    except:
        t.print_exc()

''' USAGE

seconds_of_execution = time_my_function_with_arguments(your_Function_Name, **dict_args)

#or

seconds_of_execution = time_my_function_with_arguments(your_Function_Name, *tuple_args)

print type(seconds_of_execution)
print seconds_of_execution


OUTPUT

<type 'float'>
172.976369143

'''
def time_my_function_with_arguments(function_to_time, *tuple_args, **dict_args):
    function_variable = create_function_variable_from_function_and_arguments(function_to_time, *tuple_args, **dict_args)
    return time_my_function(function_variable)

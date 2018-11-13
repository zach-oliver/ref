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

# https://www.pythoncentral.io/time-a-python-function/
# https://realpython.com/
# https://www.getdrip.com/deliveries/wuqirqpmcubzkqgsmdyc?__s=7gjuqhunc9ewzb6zvhps
# *tuple_args = if you create a tuple of the args (ie tuple_args = (1, 0, 1)) and pass it to this function,
#               it will embed those arguements within the function as a combined variable
# **dict_args = if you create a dictionary of args with the keys of the dictionary as the names of the
#               variables of the function (ie dict_vec = {'x': 1, 'y': 0, 'z': 1}), it will embed those
#               arguments within the function as a combined variable
def function_wrapper(func, tuple_args, DEBUG=True, **dict_args):
    if DEBUG:
        # tuple_args is a tuple of positional arguments,
        # because the parameter name has * prepended.
        if tuple_args: # If tuple_args is not empty.
            print 'function_timer.py|:|function_wrapper|:|tuple_args'
            print tuple_args
    
        # dict_args is a dictionary of keyword arguments,
        # because the parameter name has ** prepended.
        if dict_args: # If dict_args is not empty.
            print 'function_timer.py|:|function_wrapper|:|dict_args'
            print dict_args
    
    def wrapped():
        return func(*tuple_args, **dict_args)
    return wrapped

def time_my_function(function_to_time, setup_function='pass'):
    #t = Timer(stmt='pass', setup='pass')       # outside the try/except
    t = timeit.Timer(stmt=function_to_time, setup=setup_function)
    try:
        float_seconds = t.timeit(number=1)    # or t.repeat(...)
        return float_seconds
    except:
        t.print_exc()

''' USAGE

seconds_of_execution = time_my_function_with_arguments(your_Function_Name, **dict_args)

#or

seconds_of_execution = time_my_function_with_arguments(your_Function_Name, tuple_args)

print type(seconds_of_execution)
print seconds_of_execution


OUTPUT

<type 'float'>
172.976369143

'''
def time_my_function_with_arguments(function_to_time, tuple_args, setup_function='pass', **dict_args):
    wrapped = function_wrapper(function_to_time, tuple_args, **dict_args)
    return time_my_function(wrapped, setup_function=setup_function)

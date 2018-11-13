# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/12/18
@author: Zachary Oliver
"""
# https://www.pythoncentral.io/time-a-python-function/
# https://realpython.com/
# https://www.getdrip.com/deliveries/wuqirqpmcubzkqgsmdyc?__s=7gjuqhunc9ewzb6zvhps
# https://stackoverflow.com/questions/3394835/args-and-kwargs
# https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/
# *tuple_args = if you create a tuple of the args (ie tuple_args = (1, 0, 1)) and pass it to this function,
#               it will embed those arguements within the function as a combined variable
# **dict_args = if you create a dictionary of args with the keys of the dictionary as the names of the
#               variables of the function (ie dict_vec = {'x': 1, 'y': 0, 'z': 1}), it will embed those
#               arguments within the function as a combined variable
def create_function_variable_from_function_and_arguments(func, *tuple_args, **dict_args):
    DEBUG = True
    
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

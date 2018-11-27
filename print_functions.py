# -*- coding: utf-8 -*-
#!/usr/bin/env python2
"""
Created on 11/19/17
@author: Zachary Oliver
"""


def print_variable_highlighted(variable, str_variable_name):
	print "***********************************************************"
	print "                                                           "
	print str_variable_name + ' ' + str(type(variable)) + ' : ' + str(variable)
	print "                                                           "
	print "***********************************************************"

def print_variables_highlighted(dict_variables):
	print "***********************************************************"
	print "                                                           "
	for key, value in dict_variables.iteritems():
		print key + ' ' + str(type(value))  + ' : ' + str(value)
	print "                                                           "
	print "***********************************************************"
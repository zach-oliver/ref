# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

def df_print_columns_all_rows(df,list):
    print df[list]

def df_print_rows_all_columns(df,first,last):
    print df[first:last]

def df_print_rows_columns(df,first,last,list):
    print df[first:last,list]

def df_print_columns(df):
    for x in df.columns.values:
        print x

def df_print_top(df,top):
    print df.head(top)

def df_print_bottom(df,bottom):
    print df.tail(bottom)

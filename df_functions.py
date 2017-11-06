# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

import pandas as pd

'''********************************************
**********************READ*********************
***********************************************
'''
def df_read_csv(path):
    df = pd.read_csv(path)
    return df

def df_read_dict(dict):
    df = pd.DataFrame.from_dict(dict)
    return df

def df_read_mongodb(cursor):
    df = pd.DataFrame(list(cursor))
    return df

'''********************************************
*********************PRINT*********************
***********************************************
'''
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

def df_print_random_sample(df,size):
    print df.sample(n=size, random_state=1)

'''********************************************
**********************GET**********************
***********************************************
'''
def df_get_column_name(df, index):
    return df.columns[index]

def df_get_columns_all_rows(df,columns_list):
    return df[columns_list]

def df_get_rows_all_columns(df,first,last):
    return df[first:last]

def df_get_rows_columns(df,first_row,last_row,columns_list):
    return df[first_row:last_row,columns_list]

def df_get_row_column(df,row,column):
    return df.iloc[row][column]

def df_get_top(df,top):
    return df.head(top)

def df_get_bottom(df,bottom):
    return df.tail(bottom)

def df_get_rows_where_column_equals_value(df, column, value):
    return df.loc[(df[column] == value)]

def df_get_random_sample(df,size):
    return df.sample(n=size, random_state=1)

'''********************************************
********************COMBINE********************
***********************************************
'''
#place the dfs on top of each other with axis=0
def df_concat(df1, df2, axis=1):
    return pd.concat([df1, df2], axis=1)

'''********************************************
********************REMOVE********************
***********************************************
'''
def df_remove_column(df, column):
    return df.drop(column, axis=1, inplace=True)

def df_remove_column_by_index(df, index):
    return df.drop(df.columns[index], axis=1, inplace=True)

'''********************************************
********************RENAME********************
***********************************************
'''
def df_rename_column(df, orig_column, new_column):
    df.rename(columns={orig_column:new_column}, inplace=True)
    return df

'''********************************************
*********************COUNT*********************
***********************************************
'''
def df_print_index_counts(df):
    print df.value_counts() #always displays highest to lowest

'''********************************************
**********************SET**********************
***********************************************
'''
def df_set_index(df, column):
    df.set_index([column], inplace=True) #always displays highest to lowest

'''********************************************
********************FORMAT*********************
***********************************************
'''
def df_format_object_to_date(df, str_column):
    df[str_column] = pd.to_datetime(df[str_column])
    #df[str_column] = pd.to_datetime(df[str_column]).dt.strftime('%Y/%m/%d')

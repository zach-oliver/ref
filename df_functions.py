# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

import pandas as pd
from os_functions import create_Folders_Along_Path, evaluate_If_File_Exists

'''********************************************
**********************EXPORT*******************
***********************************************
'''
def df_export_csv(df, path, include_index=False):
    create_Folders_Along_Path(path)
    df.to_csv(path, index=include_index)

'''********************************************
**********************READ*********************
***********************************************
'''
def df_read_csv(relative_path, index_col=0):
    if evaluate_If_File_Exists(relative_path):
        df = pd.read_csv(relative_path, index_col=0)
        return df
    else:
        return None

def df_read_dict(dict):
    df = pd.DataFrame.from_dict(dict)
    return df

def df_read_mongodb(cursor):
    df = pd.DataFrame(list(cursor))
    return df

def df_read_sql(sql, conn):
    return pd.read_sql_query(sql, conn)

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

def df_get_indexes(df):
    return df.index.values

def df_get_cell(df, str_index, str_column):
    return df.at[str_index, str_column]

def df_get_list_of_list(df):
    return df.values.tolist()

'''********************************************
********************CHANGE********************
***********************************************
'''
def df_change_cell(df, str_index, str_column, value):
    df.at[str_index, str_column] = value

'''********************************************
********************COMBINE********************
***********************************************
'''
#place the dfs on top of each other with axis=0
def df_concat(df1, df2, axis=1):
    return pd.concat([df1, df2], axis=1)

# https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
# https://www.codeproject.com/KB/database/Visual_SQL_Joins/Visual_SQL_JOINS_orig.jpg
def df_merge(df1, df2):
    return pd.merge(df1, df2, left_index=True, right_index=True)

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

'''********************************************
*********************COUNT*********************
***********************************************
'''
def df_get_index_counts(df, debug=False):
    if debug:
        print df.value_counts() #always displays highest to lowest
    return df.value_counts()

def df_get_row_count(df, debug=False):
    if debug:
        print df.shape[0]
    return df.shape[0] #gives number of row count

def df_get_column_count(df, debug=False):
    if debug:
        print df.shape[1]
    return df.shape[1] #gives number of column count

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

""" replace_null
replaces null in bed with 0 and returns the data frame
variables:
df -- dataframe you want to clean
field -- name of attirbute you want to replace nulls with 0
"""
def df_format_replace_null(df, field):
    df[field].fillna(0, inplace=True)
    return df

""" replace_null
replaces null in bed with 0 and returns the data frame
variables:
df -- dataframe you want to clean
field -- name of attirbute you want to replace nulls with 0
"""
def df_format_replace_all_null(df):
    df.fillna(0, inplace=True)
    return df

'''********************************************
********************CREATE*********************
***********************************************
'''
def df_create_df_dict(keys):
    return {elem : pd.DataFrame for elem in keys}

def df_create_blank_df(df_index, df_columns_list):
    return pd.DataFrame(index=df_index, columns=df_columns_list)

def df_create_blank():
    return pd.DataFrame({'A' : []})

'''********************************************
*********************CHECK*********************
***********************************************
'''
def df_is_empty(df):
    return df.empty
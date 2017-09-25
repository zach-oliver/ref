# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 9/18/17
@author: Zachary Oliver
"""

'''********************************************
*********************LISTS*********************
***********************************************
'''

'''
EXERCISE:

7. Sort the list in reverse alphabetical order.

Bonus: Sort the list by the length of the names (shortest to longest).

'''

first_names_sorted = sorted(first_names, key=str.lower, reverse=True) #7
print first_names_sorted
first_names.sort(key=str.lower, reverse=True)
print first_names

first_names_sorted = sorted(first_names, key=len) #Bonus
print first_names_sorted
first_names.sort(key=len)
print first_names

'''********************************************
******************DICTIONARIES*****************
***********************************************
'''

'''
EXERCISE:

4. Fix 'bart' and 'lisa' so that the first letter is capitalized.

Bonus: Do this last step using a list comprehension.

'''

family = {'dad':'Homer', 'mom':'Marge', 'size':2, 'cat':'snowball ii' ,'kids':['bart', 'lisa']}

for index, item in enumerate(family['kids']): #4
    family['kids'][index] = family['kids'][index][0].upper() + family['kids'][index][1:]
print family

dict_change_value(family, 'kids', [family['kids'][index][0].upper() + family['kids'][index][1:] for index, item in enumerate(family['kids'])])
#family['kids'] = [family['kids'][index][0].upper() + family['kids'][index][1:] for index, item in enumerate(family['kids'])]
print family #Bonus

'''********************************************
*********************DATAFRAMES****************
***********************************************
'''

'''
Dataframes can use groupby
'''
df3 = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
                       'foo', 'bar', 'foo', 'foo'],
                       'B' : ['one', 'one', 'two', 'three',
                             'two', 'two', 'one', 'three'],
                       'C' : np.random.randn(8),
                       'D' : np.random.randn(8)})
df3
df3.groupby(['A','B']).sum()

'''
Concatenate Data Frames
'''
##Concatenating pandas objects together
# create a dataframe to use as an example
df2 = pd.DataFrame(np.random.randn(10,4))
df2

# Break it into pieces
pieces = [df2[:3], df2[3:7],df2[7:]]
pieces

pd.concat(pieces)

'''
Evaluate Data Frames
'''
df.A < 0 #returns list of bools with result

df[df.A < 0] # Basically a 'where' operation

# Two conditions added together
df[(df.A < 0) & (df.B > .5)]

# Two conditions ORed together
df[(df.A < -1) | (df.D > 0)]

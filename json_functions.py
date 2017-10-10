# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 10/1/17
@author: Zachary Oliver
"""

import json

'''********************************************
**********************READ*********************
***********************************************
'''
def json_read_file(path):
    with open(path, 'rU') as f:
        data = [json.loads(row) for row in f]
    return data

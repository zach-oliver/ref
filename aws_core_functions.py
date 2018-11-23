# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/16/17
@author: Zachary Oliver
"""

import os
    
'''

BOTO 3 FUNCTIONS


'''
import boto3

'''

CLIENT


'''

def create_Boto_Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return client

'''

SESSION


'''

def create_Boto_Session(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    return session


'''

AWSCLI FUNCTIONS


'''



# https://github.com/boto/boto3/issues/358
# https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html
from awscli.clidriver import create_clidriver

def aws_cli(*cmd):
    old_env = dict(os.environ)
    try:

        # Environment
        env = os.environ.copy()
        env['LC_CTYPE'] = u'en_US.UTF'
        os.environ.update(env)
        
        # Run awscli in the same process
        exit_code = create_clidriver().main(*cmd)

        # Deal with problems
        if exit_code > 0:
            raise RuntimeError('AWS CLI exited with code {}'.format(exit_code))
    finally:
        os.environ.clear()
        os.environ.update(old_env)

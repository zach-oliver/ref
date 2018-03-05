# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/16/17
@author: Zachary Oliver
"""

import boto3
import boto
import sys
import os
sys.path.insert(0, '../')
from secrets import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/
import threading


#bucket_name = 'nyymbus-website'

bucket_name = 'johnxisxawesomex123'

# reference: https://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)

bucket = conn.create_bucket(bucket_name,
    location=boto.s3.connection.Location.DEFAULT)

def upload(local_path, bucket_name, s3_path):
    client.upload_file(local_path, bucket_name, s3_path)
    return s3_path

local_directory = r'C:/Users/zoliver/Google Drive/Nyymbus/Source/website/'
destination = ''


client = boto3.client('s3')

# enumerate local files recursively
# https://gist.github.com/feelinc/d1f541af4f31d09a2ec3
for root, dirs, files in os.walk(local_directory):

  for filename in files:

    # construct the full local path
    local_path = os.path.join(root, filename)
    print 'local: ' + local_path

    relative_path = os.path.relpath(local_path, local_directory)
    s3_path = os.path.join(destination, relative_path)
    #s3_path = os.path.join(destination, filename)
    s3_path = s3_path.replace('\\','/')
    print 's3: ' + s3_path

    # relative_path = os.path.relpath(os.path.join(root, filename))
    t = threading.Thread(target = upload, args=(local_path, bucket_name, s3_path)).start()
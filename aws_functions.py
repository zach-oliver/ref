# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/16/17
@author: Zachary Oliver
"""

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

s3 = boto3.client('s3')
s3.create_bucket(Bucket='my-bucket')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file
data = open('test.jpg', 'rb')
s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)

for bucket in s3.buckets.all():
    for obj in bucket.objects.filter(Prefix='photos/'):
        print('{0}:{1}'.format(bucket.name, obj.key))

# S3 iterate over first ten buckets
for bucket in s3.buckets.limit(10):
    print(bucket.name)

# S3 iterate over all objects 100 at a time
for obj in bucket.objects.page_size(100):
    print(obj.key)

# Create a reusable Paginator
paginator = client.get_paginator('list_objects')

# Create a PageIterator from the Paginator
# http://boto3.readthedocs.io/en/latest/guide/paginators.html
page_iterator = paginator.paginate(Bucket='my-bucket')

for page in page_iterator:
    print(page['Contents'])

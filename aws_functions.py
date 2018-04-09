# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/16/17
@author: Zachary Oliver
"""

import os
# http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/
import threading

# https://docs.python.org/2/library/mimetypes.html
# used to designate the content type on S3 upload due to download vs render issue
import mimetypes

DEBUG = False

'''

BOTO FUNCTIONS


'''

# https://stackoverflow.com/questions/11426560/amazon-s3-boto-how-to-delete-folder
# boto
def delete_S3_Contents(bucket, log=False):
    threads = []
    for key in bucket.list():
        if DEBUG:
            print key
        if log:
            log.append(str(key))
        threads.append(threading.Thread(target = key.delete))
    
    # https://stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
    for t in threads:
        t.start()
    for t in threads:
        t.join()

# https://stackoverflow.com/questions/11426560/amazon-s3-boto-how-to-delete-folder
# boto
def delete_S3_Folder_Contents(bucket, folder):
    for key in bucket.list(prefix=folder):
        print key
        key.delete()

# https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3
# https://stackoverflow.com/questions/30249069/listing-contents-of-a-bucket-with-boto3
# boto
def upload_To_S3_From_S3(dest_bucket, source_bucket, log=False):
    threads = []
    for obj in source_bucket.list():
        if DEBUG:
            print obj.key
        #if log:
            #log.append(str(obj.key))
        threads.append(threading.Thread(target = dest_bucket.copy_key, args=(obj.key, source_bucket.name, obj.key)))
        
    # https://stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        
'''

BOTO 3 FUNCTIONS


'''

# boto3
# https://stackoverflow.com/questions/18296875/amazon-s3-downloads-index-html-instead-of-serving
# https://acloud.guru/forums/serverless-portfolio-with-react/discussion/-KyHqzSIDNFvxfb1Yz1D/S3%20is%20serving%20a%20download%20of%20my%20index.html%20instead%20of%20displaying%20it%20in%20the%20browser
# https://github.com/robin-acloud/my-portfolio/commit/61ce4cb2d8a5754912b677fa996771a8e7f58d56
def upload_File_To_S3_From_Local(boto3_client, local_path, bucket_name, s3_path):
    if DEBUG:
        print str(mimetypes.guess_type(local_path)[0])
    boto3_client.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ContentType': mimetypes.guess_type(local_path)[0]})

# boto3
def upload_Directory_To_S3_From_Local(local_directory, destination, boto3_client, bucket_name):
    threads = []
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
            #upload_File_To_S3_From_Local(boto3_client, local_path, bucket_name, s3_path)
            threads.append(threading.Thread(target = upload_File_To_S3_From_Local, args=(boto3_client, local_path, bucket_name, s3_path)))
    
    # https://stackoverflow.com/questions/11968689/python-multithreading-wait-till-all-threads-finished
    for t in threads:
        t.start()
    for t in threads:
        t.join()

# boto3
# https://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket
def delete_S3_Object(boto3_client, bucket_name, bucket_object_key):
    print bucket_object_key
    boto3_client.delete_object(Bucket=bucket_name, Key=bucket_object_key)

# https://stackoverflow.com/questions/33104579/boto3-s3-folder-not-getting-deleted
def delete_S3_Folder_Contents3(s3_resource, bucket_name, folder_name):
    
    bucket = s3_resource.Bucket(bucket_name)
    
    objects_to_delete = []
    for obj in bucket.objects.filter(Prefix=folder_name):
        objects_to_delete.append({'Key': obj.key})
    
    bucket.delete_objects(
        Delete={
            'Objects': objects_to_delete
        }
)

# boto3
# https://github.com/aws/aws-cli/issues/2603
def create_S3_Bucket(boto3_client, bucket_name, bucket_region):
    #s3 = boto3.client('s3')
    boto3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': bucket_region})
# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on 11/16/17
@author: Zachary Oliver
"""

import os

# https://docs.python.org/2/library/mimetypes.html
# used to designate the content type on S3 upload due to download vs render issue
import mimetypes

from os_functions import create_Folders_Along_Path
from thread_class import Bounded_Semaphore_Thread

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
        threads.append(Bounded_Semaphore_Thread(key.delete, name=("delete_S3_Contents:%s" % str(key))))
    
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
        threads.append(Bounded_Semaphore_Thread(dest_bucket.copy_key, name=("upload_To_S3_From_S3:%s" % str(obj.key)), args=(obj.key, source_bucket.name, obj.key)))
        
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
def upload_Directory_To_S3_From_Local(local_directory, destination, boto3_client, bucket_name, DEBUG=False):
    threads = []
    # enumerate local files recursively
    # https://gist.github.com/feelinc/d1f541af4f31d09a2ec3
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            # construct the full local path
            local_path = os.path.join(root, filename)
            if DEBUG:
                print 'local: ' + local_path
        
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(destination, relative_path)
            #s3_path = os.path.join(destination, filename)
            s3_path = s3_path.replace('\\','/')
            if DEBUG:
                print 's3: ' + s3_path
        
            # relative_path = os.path.relpath(os.path.join(root, filename))
            #upload_File_To_S3_From_Local(boto3_client, local_path, bucket_name, s3_path)
            threads.append(Bounded_Semaphore_Thread(upload_File_To_S3_From_Local, name=("upload_Directory_To_S3_From_Local:%s" % str(filename)), args=(boto3_client, local_path, bucket_name, s3_path)))
    
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
    some_objects_to_delete = []
    for obj in bucket.objects.filter(Prefix=folder_name):
        objects_to_delete.append({'Key': obj.key})
    
    if len(objects_to_delete) > 1000:
        for i in range(0,1000):
            some_objects_to_delete.append(objects_to_delete.pop(0))
        bucket.delete_objects(
                Delete={
                        'Objects': objects_to_delete
                        }
                )
        bucket.delete_objects(
                Delete={
                        'Objects': some_objects_to_delete
                        }
                )
    elif objects_to_delete:
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

# https://stackoverflow.com/questions/31918960/boto3-to-download-all-files-from-a-s3-bucket/31929277
def download_S3_Bucket(boto3_client, str_bucket_name, str_bucket_path, str_local_relative_target):
    """
    Downloads recursively the given S3 path to the target directory.
    :param client: S3 client to use.
    :param bucket: the name of the bucket to download from
    :param path: The S3 directory to download.
    :param target: the local directory to download the files to.
    """

    # Handle missing / at end of prefix
    if not str_bucket_path.endswith('/'):
        str_bucket_path += '/'

    paginator = boto3_client.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=str_bucket_name, Prefix=str_bucket_path):
        # Download each file individually
        for key in result['Contents']:
            # Calculate relative path
            rel_path = key['Key'][len(str_bucket_path):]
            # Skip paths ending in /
            if not key['Key'].endswith('/'):
                local_file_path = os.path.join(str_local_relative_target, rel_path)
                # Make sure directories exist
                local_file_dir = os.path.dirname(local_file_path)
                create_Folders_Along_Path(local_file_dir)
                boto3_client.download_file(str_bucket_name, key['Key'], local_file_path)

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

# FROM_LOCAL_SOURCE: Used to designate whether you want to sync from the local source to S3 or from S3 to local
def sync_S3_Bucket_With_Local_Dir(str_full_source_path, str_bucket_name, str_bucket_path, FROM_LOCAL_SOURCE=True, DELETE_DIFFERENCES=False):
    command = ''
    if FROM_LOCAL_SOURCE:
        commands = ['s3', 'sync', str_full_source_path, 's3://%s/%s' % (str_bucket_name, str_bucket_path), '--exact-timestamps']
        if DELETE_DIFFERENCES:
            commands.append('--delete')
        
        # print the command
        for c in commands:
            command = command + c + " "
        print command
        
        aws_cli(commands)
    else:
        commands = ['s3', 'sync', 's3://%s/%s' % (str_bucket_name, str_bucket_path), str_full_source_path, '--exact-timestamps']
        if DELETE_DIFFERENCES:
            commands.append('--delete')
        
        # print the command
        for c in commands:
            command = command + c + " "
        print command
        
        aws_cli(commands)

def sync_S3_Bucket_With_S3_Bucket(str_source_bucket_name, str_source_bucket_path, str_dest_bucket_name, str_dest_bucket_path, DELETE_DIFFERENCES=False):
    commands = ['s3', 'sync', 's3://%s/%s' % (str_source_bucket_name, str_source_bucket_path), 's3://%s/%s' % (str_dest_bucket_name, str_dest_bucket_path), '--exact-timestamps']
    if DELETE_DIFFERENCES:
        commands.append('--delete')
    
    # print the command
    command = ''
    for c in commands:
        command = command + c + " "
    print command
    
    aws_cli(commands)
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

from os_functions import create_Folders_Along_Path, convert_To_Date_Time
from thread_class import Bounded_Semaphore_Thread

    
'''

BOTO 3 FUNCTIONS


'''
import boto3
import botocore

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

S3


'''

# ************
# UPLOAD
# ************

# https://stackoverflow.com/questions/18296875/amazon-s3-downloads-index-html-instead-of-serving
# https://acloud.guru/forums/serverless-portfolio-with-react/discussion/-KyHqzSIDNFvxfb1Yz1D/S3%20is%20serving%20a%20download%20of%20my%20index.html%20instead%20of%20displaying%20it%20in%20the%20browser
# https://github.com/robin-acloud/my-portfolio/commit/61ce4cb2d8a5754912b677fa996771a8e7f58d56
def upload_File_To_S3_From_Local(str_bucket_name, str_local_dir, str_bucket_object_key, DEBUG=True):
    if DEBUG:
        print 'aws_functions.py --> upload_File_To_S3: START'
        print 'aws_functions.py --> upload_File_To_S3: str_bucket_name=%s' % (str(str_bucket_name))
        print 'aws_functions.py --> upload_File_To_S3: str_local_dir=%s' % (str(str_local_dir))
        print 'aws_functions.py --> upload_File_To_S3: str_local_dir type is %s' % (str(mimetypes.guess_type(str_local_dir)[0]))
        print 'aws_functions.py --> upload_File_To_S3: str_bucket_object_key=%s' % (str(str_bucket_object_key))
    
    s3_bucket = boto3.resource('s3').Bucket(str_bucket_name)
    
    if DEBUG:
        print 'aws_functions.py --> upload_File_To_S3: s3 BUCKET RESOURCE INSTANTIATED'
    try:
        s3_bucket.upload_file(str_local_dir, str_bucket_object_key, ExtraArgs={'ContentType': mimetypes.guess_type(str_local_dir)[0]})
    except botocore.exceptions.ClientError as e:
        #
        #
        # NEED BETTER ERROR HANDLING
        #
        #
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
            return False
        else:
            raise
            return False
        
    if DEBUG:
        print 'aws_functions.py --> upload_File_To_S3: s3 BUCKET OBJECT CREATED'
        print 'aws_functions.py --> upload_File_To_S3: FINISH'
    
    return True

def upload_Directory_To_S3_From_Local(local_directory, destination, boto3_client, bucket_name, DEBUG=True):
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

# ************
# DELETE
# ************

# https://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
def delete_S3_Object(str_bucket_name, str_bucket_object_key, DEBUG=True):
    if DEBUG:
        print 'aws_functions.py --> delete_S3_Object: START'
        print 'aws_functions.py --> delete_S3_Object: str_bucket_name=%s' % (str(str_bucket_name))
        print 'aws_functions.py --> delete_S3_Object: str_bucket_object_key=%s' % (str(str_bucket_object_key))
    s3_bucket = boto3.resource('s3').Bucket(str_bucket_name)
    if DEBUG:
        print 'aws_functions.py --> delete_S3_Object: s3 RESOURCE INSTANTIATED'
    try:
        s3_bucket.delete_objects(
                Delete={
                        'Objects': [{'Key': str_bucket_object_key}]
                        }
                )
        # s3_bucket.delete_object(Bucket=bucket_name, Key=bucket_object_key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if DEBUG:
                print 'aws_functions.py --> delete_S3_Object: s3 OBJECT DOESNT EXIST'
                print 'aws_functions.py --> delete_S3_Object: FINISH'
            return False
        else:
            raise
            return False
        
    if DEBUG:
        print 'aws_functions.py --> delete_S3_Object: s3 OBJECT DELETED'
        print 'aws_functions.py --> delete_S3_Object: FINISH'
    
    return True

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



# ************
# CREATE
# ************

# https://github.com/aws/aws-cli/issues/2603
def create_S3_Bucket(boto3_client, bucket_name, bucket_region):
    #s3 = boto3.client('s3')
    boto3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': bucket_region})



# ************
# DOWNLOAD
# ************

def download_S3_Object(str_bucket_name, str_bucket_object_key, str_local_dir, DEBUG=False):
    if DEBUG:
        print 'aws_functions.py --> download_S3_Object: START'
        print 'aws_functions.py --> download_S3_Object: str_bucket_name=%s' % (str(str_bucket_name))
        print 'aws_functions.py --> download_S3_Object: str_bucket_object_key=%s' % (str(str_bucket_object_key))
        print 'aws_functions.py --> download_S3_Object: str_local_dir=%s' % (str(str_local_dir))
    else:
        print 'download_S3_Object: s3://%s/%s --> %s' % (str(str_bucket_name), str(str_bucket_object_key), str(str_local_dir))
    
    s3_bucket = boto3.resource('s3').Bucket(str_bucket_name)
    
    if DEBUG:
        print 'aws_functions.py --> download_S3_Object: s3 RESOURCE INSTANTIATED'
    
    try:
        s3_bucket.download_file(str_bucket_object_key, str_local_dir)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if DEBUG:
                print 'aws_functions.py --> download_S3_Object: s3 OBJECT DOESNT EXIST'
                print 'aws_functions.py --> download_S3_Object: FINISH'
            return False
        else:
            raise
            return False
        
    if DEBUG:
        print 'aws_functions.py --> download_S3_Object: s3 BUCKET OBJECT CREATED'
        print 'aws_functions.py --> download_S3_Object: FINISH'
    
    return True

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

# ************
# INFO
# ************
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.ServiceResource.ObjectSummary
def get_S3_Bucket_Object_Info(str_bucket_name, str_bucket_object_key, DEBUG=False):
    if DEBUG:
        print 'aws_functions.py --> get_S3_Bucket_Object_Info: START'
        print 'aws_functions.py --> get_S3_Bucket_Object_Info: str_bucket_name=%s' % (str(str_bucket_name))
        print 'aws_functions.py --> get_S3_Bucket_Object_Info: str_bucket_object_key=%s' % (str(str_bucket_object_key))
    else:
        print 'get_S3_Bucket_Object_Info: s3://%s/%s' % (str(str_bucket_name), str(str_bucket_object_key))
    
    try:
        s3_object_summary = boto3.resource('s3').ObjectSummary(str_bucket_name, str_bucket_object_key)
    
        if DEBUG:
            print 'aws_functions.py --> get_S3_Bucket_Object_Info: s3 OBJECT SUMMARY INSTANTIATED'
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if DEBUG:
                print 'aws_functions.py --> get_S3_Bucket_Object_Info: s3 OBJECT DOESNT EXIST'
                print 'aws_functions.py --> get_S3_Bucket_Object_Info: FINISH'
            return False
        else:
            raise
            return False
        
    if DEBUG:
        print 'aws_functions.py --> get_S3_Bucket_Object_Info: s3 BUCKET OBJECT SUMMARY COLLECTED'
        print 'aws_functions.py --> get_S3_Bucket_Object_Info: FINISH'
    
    return s3_object_summary

def get_S3_Bucket_Object_Last_Modified_Date(str_bucket_name, str_bucket_object_key, DEBUG=False):
    if DEBUG:
        print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: START'
        print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: str_bucket_name=%s' % (str(str_bucket_name))
        print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: str_bucket_object_key=%s' % (str(str_bucket_object_key))
    else:
        print 'get_S3_Bucket_Object_Last_Modified_Date: s3://%s/%s' % (str(str_bucket_name), str(str_bucket_object_key))
    
    try:
        if DEBUG:
            print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date --> get_S3_Bucket_Object_Info'
        last_modified = get_S3_Bucket_Object_Info(str_bucket_name, str_bucket_object_key).last_modified
        print 'BEFORE'
        print type(last_modified)
        print str(last_modified)
        last_modified = convert_To_Date_Time(last_modified)
        print 'AFTER'
        print type(last_modified)
        print str(last_modified)
    
        if DEBUG:
            print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date --> get_S3_Bucket_Object_Info: FINISHED'
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            if DEBUG:
                print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: s3 OBJECT DOESNT EXIST'
                print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: FINISH'
            return False
        else:
            raise
            return False
    
    if DEBUG:
        print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: s3 BUCKET OBJECT LAST MODIFIED DATE COLLECTED'
        print 'aws_functions.py --> get_S3_Bucket_Object_Last_Modified_Date: FINISH'
    
    return last_modified

# ************
# SYNC
# ************

# FROM_LOCAL_SOURCE: Used to designate whether you want to sync from the local source to S3 or from S3 to local
# issue: --exact-timestamps didn't work as expected: https://github.com/aws/aws-cli/issues/2000
def sync_S3_Bucket_With_Local_Dir(str_full_source_path, str_bucket_name, str_bucket_path, FROM_LOCAL_SOURCE=True, DELETE_DIFFERENCES=False):
    command = ''
    if FROM_LOCAL_SOURCE:
        commands = ['s3', 'sync', str_full_source_path, 's3://%s/%s' % (str_bucket_name, str_bucket_path)]
        if DELETE_DIFFERENCES:
            commands.append('--delete')
        
        # print the command
        for c in commands:
            command = command + c + " "
        print command
        
        aws_cli(commands)
    else:
        commands = ['s3', 'sync', 's3://%s/%s' % (str_bucket_name, str_bucket_path), str_full_source_path]
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

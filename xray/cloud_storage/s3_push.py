import os
import sys
from typing import List,Tuple
import boto3
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket
from xray.logger import logging

from xray.exception import XRayException


class S3PushOps:

    def __init__(self):
        self.s3_client=boto3.client
        self.s3_resource=boto3.resource

    def upload_file(self,
        from_filename:str,to_filename:str,
        bucket_name:str,remove:bool= True):

        logging.info("Entered the upload_file method of S3Operations class")

        try:
            pass
        except Exception as e:
            raise XRayException(e, sys)




            


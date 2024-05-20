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
        self.s3_client=boto3.client("s3")
        self.s3_resource=boto3.resource("s3")

    def upload_file(self,
        from_filename:str,to_filename:str,
        bucket_name:str,remove:bool= True):

        logging.info("Entered the upload_file method of S3Operations class")

        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )
            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
            logging.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise XRayException(e, sys)




            


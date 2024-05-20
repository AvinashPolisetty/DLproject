from xray.exception import XRayException
from xray.logger import logging
from xray.cloud_storage.s3_push import S3PushOps
import sys

class ModelPusher:

    def __init__(self,model_pusher_config):
        self.model_push_config=model_pusher_config
        self.s3_ops=S3PushOps()


    
    def initiate_model_pusher(self):

        try:
            logging.info("Entered initiate_model_pusher method of Modelpusher class")
            self.s3_ops.upload_file(
                "models\model_trainer\model.pt",
                "model.pt",
                bucket_name="dlproj1",
                remove = False
            )
            logging.info("Uploaded best model to s3 bucket")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")


        except Exception as e:
            raise XRayException(e,sys)
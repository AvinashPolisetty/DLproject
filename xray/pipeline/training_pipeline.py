import sys
from xray.logger import logging
from xray.exception import XRayException
from xray.components.data_ingestion import DataIngestion
from xray.components.data_transformation import DataTransformation
from xray.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from xray.entity.config_entity import DataIngestionConfig,DataTransformationConfig


class TrainPipeline:

    def __init__(self):
        self.data_ingestion=DataIngestionConfig()
        self.data_transformation=DataTransformationConfig()

    
    def start_data_ingestion(self):
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from s3 bucket")

            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

            logging.info("Got the train_set and test_set from s3")

            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise XRayException(e,sys)
        
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact)->DataTransformationArtifact:
        logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation=DataTransformation(data_transformation_config=self.data_transformation,
                                                   data_ingestion_artifact=DataIngestionArtifact)
            
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )

            return data_transformation_artifact
        except Exception as e:
            raise XRayException(e,sys)
        

    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()
            data_transformation_artifact: DataTransformationArtifact = (
                self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )
        except Exception as e:
            raise XRayException(e,sys)

        




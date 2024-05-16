import sys
from xray.logger import logging
from xray.exception import XRayException
from xray.components.data_ingestion import DataIngestion
from xray.entity.artifact_entity import DataIngestionArtifact
from xray.entity.config_entity import DataIngestionConfig
from xray.pipeline.training_pipeline import TrainPipeline


def start_training():
    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
    except Exception as e:
        raise XRayException(e,sys)
    

if __name__=="__main__":
    start_training()
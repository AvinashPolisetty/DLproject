import sys
from xray.logger import logging
from xray.exception import XRayException
from xray.components.data_ingestion import DataIngestion
from xray.components.data_transformation import DataTransformation
from xray.components.model_training import ModelTrainer
from xray.components.model_evaluation import ModelEvaluation
from xray.components.model_pusher import ModelPusher
from xray.entity.artifact_entity import (DataIngestionArtifact,DataTransformationArtifact,
                                         ModelTrainerArtifact,ModelEvaluationArtifact,
                                         ModelPusherArtifact)
from xray.entity.config_entity import (DataIngestionConfig,DataTransformationConfig,
                                       ModelTrainerConfig,ModelEvaluationConfig,ModelPusherConfig)


class TrainPipeline:

    def __init__(self):
        self.data_ingestion=DataIngestionConfig()
        self.data_transformation=DataTransformationConfig()
        self.model_training=ModelTrainerConfig()
        self.model_evaluation=ModelEvaluationConfig()
        self.model_pusher_config=ModelPusherConfig()

    
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
                                                   data_ingestion_artifact=data_ingestion_artifact)
            
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )

            return data_transformation_artifact
        except Exception as e:
            raise XRayException(e,sys)
        
    
    def start_model_training(self,data_transform_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            logging.info("Entered the start_model_trainer method of TrainPipeline class")

            model_trainer=ModelTrainer(data_transformation_artifact=data_transform_artifact,
                         model_train_config=self.model_training)
            
            model_trainer_artifact=model_trainer.initiate_model_trainer()

            logging.info("Exited the start_model_trainer method of TrainPipeline class")

            return model_trainer_artifact
        
        except Exception as e:
            raise XRayException(e, sys)


            
    def start_model_evaluation(self,model_train_artifact:ModelTrainerArtifact,
                            data_transform_artifact:DataTransformationArtifact)->ModelEvaluationArtifact:
        logging.info("Entered the start_model_evaluation method of TrainPipeline class")

        try:
            model_evaluation = ModelEvaluation(
                data_transform_artifact=data_transform_artifact,
                model_eval=self.model_evaluation,
                model_train_artifact=model_train_artifact,
            )

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

            logging.info(
                "Exited the start_model_evaluation method of TrainPipeline class"
            )

            return model_evaluation_artifact

        except Exception as e:
            raise XRayException(e, sys)

       
    def start_model_pusher(self)->ModelPusherArtifact:

        try:
            logging.info("Entered the start_model_pusher method of TrainPipeline class")

            model_pusher = ModelPusher(model_pusher_config=self.model_pusher_config)
            model_pusher_artifact=model_pusher.initiate_model_pusher()

            return model_pusher_artifact

        except Exception as e:
            raise  XRayException(e,sys)

    def run_pipeline(self) -> None:
        logging.info("Entered the run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            data_transformation_artifact: DataTransformationArtifact = (
                self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            model_trainer_artifact:ModelTrainerArtifact=self.start_model_training(
                data_transform_artifact=data_transformation_artifact)
            

            model_eval_artifact:ModelEvaluationArtifact = self.start_model_evaluation(
                model_train_artifact=model_trainer_artifact,
                data_transform_artifact=data_transformation_artifact
            )

            model_pusher_artifact:ModelPusherArtifact = self.start_model_pusher()

            logging.info("Exited the run_pipeline method of TrainPipeline class")


            
        except Exception as e:
            raise XRayException(e,sys)

        




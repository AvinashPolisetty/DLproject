from xray.constant.training_pipeline import *
from xray.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from xray.entity.config_entity import DataTransformationConfig
from xray.exception import XRayException
from xray.logger import logging
from torch.utils.data import DataLoader,Dataset
from torchvision import transforms
from torchvision.datasets import ImageFolder
import sys
from typing import Tuple
import os
import joblib

class DataTransformation:

    def __init__(self,
                data_transformation_config:DataTransformationConfig,
                data_ingestion_artifact:DataIngestionArtifact):
        
        self.data_transform=data_transformation_config
        self.data_ingestion_artifacts=data_ingestion_artifact

    
    def trainig_data_transformation(self)->transforms.Compose:
        try:
            logging.info(
                "Entered the transforming_training_data method of Data transformation class")
             
            train_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transform.resize),
                    transforms.CenterCrop(self.data_transform.CENTERCROP),
                    transforms.ColorJitter(self.data_transform.color_jitter_transform),
                    transforms.RandomHorizontalFlip(),
                    transforms.RandomRotation(
                        self.data_transformation_config.RANDOMROTATION
                    ),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transformation_config.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_training_data method of Data transformation class"
            )

            return train_transform

        except Exception as e:
            raise XRayException(e,sys)
        

    def testing_data_transformation(self):
        
        logging.info(
            "Entered the transforming_testing_data method of Data transformation class"
        )

        try:
            test_transform: transforms.Compose = transforms.Compose(
                [
                    transforms.Resize(self.data_transform.resize),
                    transforms.CenterCrop(self.data_transfor.CENTERCROP),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        **self.data_transform.normalize_transforms
                    ),
                ]
            )

            logging.info(
                "Exited the transforming_testing_data method of Data transformation class"
            )

            return test_transform
        except Exception as e:
            raise XRayException(e,sys)
        
    
    def data_loader(self,train_transform:transforms.Compose,
            test_transform:transforms.Compose)-> Tuple[DataLoader,DataLoader]:
        
        try:
            logging.info("Entered the data_loader method of Data transformation class")

            train_data:Dataset=ImageFolder(
                os.path.join(self.data_ingestion_artifacts.train_file_path,
                transform=train_transform)
            )

            test_data: Dataset = ImageFolder(
                os.path.join(self.data_ingestion_artifact.test_file_path),
                transform=test_transform,
            )

            logging.info("Created train data and test data paths")

            train_loader:DataLoader= DataLoader(
                train_data,**self.data_transform.data_loader_params
            )

            test_loader:DataLoader=DataLoader(
                test_data,**self.data_transform.data_loader_params
            )

            logging.info("Exited the data_loader method of Data transformation class")

            return train_loader, test_loader

        except Exception as e:
            raise XRayException(e,sys)
        

    def initiate_data_transformation(self)->DataIngestionArtifact:
        try:
            logging.info(
                "Entered the initiate_data_transformation method of Data transformation class"
            )

            train_transform: transforms.Compose = self.trainig_data_transformation()

            test_transform: transforms.Compose = self.testing_data_transformation()

            os.makedirs(self.data_transform.artifact_dir, exist_ok=True)

            joblib.dump(
                train_transform, self.data_transform.train_transforms_file
            )

            joblib.dump(
                test_transform, self.data_transform.test_transforms_file
            )

            train_loader, test_loader = self.data_loader(
                train_transform=train_transform, test_transform=test_transform
            )

            data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                transformed_train_object=train_loader,
                transformed_test_object=test_loader,
                train_transform_file_path=self.data_transform.train_transforms_file,
                test_transform_file_path=self.data_transform.test_transforms_file,
            )

            logging.info(
                "Exited the initiate_data_transformation method of Data transformation class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise XRayException(e, sys)

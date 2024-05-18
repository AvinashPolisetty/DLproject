from xray.constant.training_pipeline import *
from xray.entity.artifact_entity import (DataIngestionArtifact,DataTransformationArtifact,
                                         ModelTrainerArtifact)
from xray.entity.config_entity import ModelTrainerConfig
from xray.exception import XRayException
from xray.logger import logging
import sys
import os
import bentoml
import joblib
import torch
import torch.nn.functional as F
from torch.nn import Module
from torch.optim import Optimizer
from torch.optim.lr_scheduler import StepLR,_LRScheduler
from tqdm import tqdm
from xray.model.arch import Net

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_train_config:ModelTrainerConfig):
        
        self.data_transform:DataTransformationArtifact=(data_transformation_artifact)
        self.model_train:ModelTrainerConfig=model_train_config
        self.model:Module = Net()


    def train(self,optimizer:Optimizer)->None:
        logging.info("Entered the train method of Model trainer class")

        try:
            self.model.train()
            pbar = tqdm(self.data_transform.transformed_train_object)

            correct: int = 0

            processed = 0

            for batch_idx,(data,target) in enumerate(pbar):
                data, target = data.to(DEVICE), target.to(DEVICE)
                optimizer.zero_grad()

                y_pred = self.model(data)

                # Calculating loss given the prediction
                loss = F.nll_loss(y_pred, target)

                # Backprop
                loss.backward()

                optimizer.step()

                # get the index of the log-probability corresponding to the max value
                pred = y_pred.argmax(dim=1, keepdim=True)

                correct += pred.eq(target.view_as(pred)).sum().item()

                processed += len(data)

                pbar.set_description(
                    desc=f"Loss={loss.item()} Batch_id={batch_idx} Accuracy={100*correct/processed:0.2f}"
                )

            logging.info("Exited the train method of Model trainer class")

        except Exception as e:
            raise XRayException(e,sys)
        

    def test(self)->None:
        try:
            logging.info("Entered the test method of Model trainer class")

            self.model.eval()

            test_loss: float = 0.0

            correct: int = 0

            with torch.no_grad():
                for (
                    data,
                    target,
                ) in self.data_transform.transformed_test_object:
                    data, target = data.to(DEVICE), target.to(DEVICE)

                    output = self.model(data)

                    test_loss += F.nll_loss(output, target, reduction="sum").item()

                    pred = output.argmax(dim=1, keepdim=True)

                    correct += pred.eq(target.view_as(pred)).sum().item()

                test_loss /= len(
                    self.data_transform.transformed_test_object.dataset
                )

                print(
                    "Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)\n".format(
                        test_loss,
                        correct,
                        len(
                            self.data_transform.transformed_test_object.dataset
                        ),
                        100.0
                        * correct
                        / len(
                            self.data_transform.transformed_test_object.dataset
                        ),
                    )
                )

            logging.info(
                "Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.2f}%)".format(
                    test_loss,
                    correct,
                    len(
                        self.data_transform.transformed_test_object.dataset
                    ),
                    100.0
                    * correct
                    / len(
                        self.data_transform.transformed_test_object.dataset
                    ),
                )
            )

            logging.info("Exited the test method of Model trainer class")
        except Exception as e:
            raise XRayException(e,sys)


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logging.info(
                "Entered the initiate_model_trainer method of Model trainer class"
            )

            model: Module = self.model.to(self.model_train.device)

            optimizer: Optimizer = torch.optim.SGD(
                model.parameters(), **self.model_train.optimizer_params
            )

            scheduler: _LRScheduler = StepLR(
                optimizer=optimizer, **self.model_train.scheduler_params
            )

            for epoch in range(1, self.model_train.epochs + 1):
                print("Epoch : ", epoch)

                self.train(optimizer=optimizer)

                optimizer.step()

                scheduler.step()

                self.test()

            os.makedirs(self.model_train.artifact_dir, exist_ok=True)

            torch.save(model, self.model_train.trained_model_path)

            train_transforms_obj = joblib.load(
                self.data_transform.train_transform_file_path
            )

            bentoml.pytorch.save_model(
                name=self.model_train.trained_bentoml_model_name,
                model=model,
                custom_objects={
                    self.model_train.train_transform_key: train_transforms_obj
                },
            )

            model_trainer_artifact: ModelTrainerArtifact = ModelTrainerArtifact(
                trained_model_path=self.model_train.trained_model_path
            )

            logging.info(
                "Exited the initiate_model_trainer method of Model trainer class"
            )

            return model_trainer_artifact

        except Exception as e:
            raise XRayException(e, sys)
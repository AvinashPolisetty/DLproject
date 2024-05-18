from datetime import datetime
from typing import List,Tuple

import torch

TIMESTAMP: datetime = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


# Data Ingestion Constants
ARTIFACT_DIR: str = "artifacts"

BUCKET_NAME: str = "dlproj1"

S3_DATA_FOLDER: str = "data"


# data trasnforamtion
CLASS_LABEL_1: str = "NORMAL"

CLASS_LABEL_2: str = "PNEUMONIA"

brightness: Tuple[float, float] = (0.875, 1.125)

contrast: Tuple[float, float] = (0.5, 1.5)

saturation: Tuple[float, float] = (0.5, 1.5)

hue: Tuple[float, float] = (-0.05, 0.05)

RESIZE: int = 224

CENTERCROP: int = 224

RANDOMROTATION: int = 10

NORMALIZE_LIST_1: List[int] = [0.485, 0.456, 0.406]

NORMALIZE_LIST_2: List[int] = [0.229, 0.224, 0.225]

TRAIN_TRANSFORMS_KEY: str = "xray_train_transforms"

TRAIN_TRANSFORMS_FILE: str = "train_transforms.pkl"

TEST_TRANSFORMS_FILE: str = "test_transforms.pkl"

BATCH_SIZE: int = 2

SHUFFLE: bool = False

PIN_MEMORY: bool = True


#model trainer constants

TRAINED_MODEL_DIR: str = "trained_model"

TRAINED_MODEL_NAME: str = "model.pt"

DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

STEP_SIZE: int = 6

GAMMA: int = 0.5

EPOCH: int = 1

BENTOML_MODEL_NAME: str = "xray_model"

BENTOML_SERVICE_NAME: str = "xray_service"

BENTOML_ECR_URI: str = "xray_bento_image"

PREDICTION_LABEL: dict = {"0": CLASS_LABEL_1, 1: CLASS_LABEL_2}
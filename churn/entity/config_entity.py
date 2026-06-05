

from churn.constants import *
import os
from datetime import datetime
from dataclasses import dataclass

TimeFrame = f"{datetime.now().strftime('%d-%B-%Y-%H-%M-%S')}"

artifcat = "Artifcat"

main_artifact = os.path.join(artifcat,TimeFrame)


@dataclass
class DataIngestionConfig:

    data_ingestion_folder :str = os.path.join(main_artifact,DATA_INGRSTION_MAIN_FOLDER)
    data_ingestion_raw_file_path:str = os.path.join(data_ingestion_folder,DATA_INGESTION_RAW_DATA_FOLDER,DATA_INGESTION_RAW_DATA_FILE_PATH)
    data_ingestion_train_file_path :str = os.path.join(data_ingestion_folder,DATA_INGESTION_INGESTED_FOLDER,DATA_INGESTION_INGESTED_TRAIN_FILE)
    data_ingestion_test_file_path :str = os.path.join(data_ingestion_folder,DATA_INGESTION_INGESTED_FOLDER,DATA_INGESTION_INGESTED_TEST_FILE)
    train_test_split_ratio:float = train_test_split_ratio


@dataclass
class DataValidationConfig:

    data_validation_main_folder :str = os.path.join(main_artifact,DATA_VALIDATION_MAIN_FOLDER)
    data_validation_status_file :str = os.path.join(data_validation_main_folder,DATA_VALIDATION_STATUS_FOLDER,DATA_VALIDATION_STATUS_FILE)
    data_validation_drift_report_file :str = os.path.join(data_validation_main_folder,DATA_VALIDATION_DRIFT_REPORT_FOLDER,DATA_VALIDATION_DRIFT_REPORT_FILE)
    
@dataclass
class DataTransformationConfig:

    data_transformation_main_folder :str = os.path.join(main_artifact,DATA_TRANSFORMATION_MAIN_FOLDER)
    data_transformation_processed_file_path : str = os.path.join(data_transformation_main_folder,DATA_TRANSFORMATION_PREPROCESS_OBJ_FOLDER,DATA_TRANSFORMATION_PROPROCESS_OBJ_FILE)
    data_transformation_train_file_path : str = os.path.join(data_transformation_main_folder,DATA_TRANSFORMATION_TRANSFORMED_FOLDER,DATA_TRANSFORMATION_TRAIN_FILE_NAME)
    data_transformation_test_file_path : str = os.path.join(data_transformation_main_folder,DATA_TRANSFORMATION_TRANSFORMED_FOLDER,DATA_TRANSFORMATION_TEST_FILE_NAME)


@dataclass
class ModelTrainerConfig:

    model_trainer_main_fodler :str = os.path.join(main_artifact,MODEL_TRAINER_MAIN_FOLDER)
    model_trainer_trained_path :str = os.path.join(model_trainer_main_fodler,MODEL_TRAINER_TRAINED_FOLDER,MODEL_TRAINDER_TRAINED_OBJECT)



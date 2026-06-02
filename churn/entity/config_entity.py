

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
    
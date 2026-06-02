

import sys
import pandas as pd 
from churn.exception import CustomException
from churn.logger import logger
from churn.data_access.churn_data import ChurnData
from sklearn.model_selection import train_test_split
from churn.entity.config_entity import DataIngestionConfig
from churn.entity.artifact_entity import DataIngestionArtifact
from churn.constants import COLLECTION_NAME
from churn.utils.main_utils import create_folder_path





class DataIngetion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):

        self.data_ingestion_config = data_ingestion_config
    
    def extract_data_and_save(self,collection_name):

        try:
            logger.info(f"Entered into extract_data_and_save function in DataIngestion class")

            churn_data = ChurnData()

            data = churn_data.extract_data_from_mongodb(collection_name=collection_name)

            # now save this data into date ingestion folder

            create_folder_path(self.data_ingestion_config.data_ingestion_raw_file_path)

            data.to_csv(self.data_ingestion_config.data_ingestion_raw_file_path,index=False)

            logger.info(f"Data saved into {self.data_ingestion_config.data_ingestion_raw_file_path}")

            return self.data_ingestion_config.data_ingestion_raw_file_path

        except Exception as e:
            raise CustomException(e,sys)
    
    def split_data_into_train_test(self,path:str):

        try:

            data = pd.read_csv(path)

            logger.info("Entered into split_data_into_train_test function in dataIngestion class")

            train,test = train_test_split(data,test_size=self.data_ingestion_config.train_test_split_ratio,shuffle=True)

            # now save thsi test and train into data ingestion path

            create_folder_path(self.data_ingestion_config.data_ingestion_train_file_path)

            train.to_csv(self.data_ingestion_config.data_ingestion_train_file_path,index=False)
            test.to_csv(self.data_ingestion_config.data_ingestion_test_file_path,index=False)

            logger.info(f"Both train and test saved into Their paths")

            return self.data_ingestion_config.data_ingestion_train_file_path,self.data_ingestion_config.data_ingestion_test_file_path

        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_ingetion(self)->DataIngestionArtifact:

        try:

            logger.info("Entered into initiate_data_ingetion function in DataIngestion class")
            
            raw_path = self.extract_data_and_save(collection_name=COLLECTION_NAME)

            train_path,test_path = self.split_data_into_train_test(path=raw_path)

            data_ingestion_artifact = DataIngestionArtifact(
                raw_file_path =  raw_path,
                train_file_path = train_path,
                test_file_path =  test_path
            )

            return data_ingestion_artifact

        
        except Exception as e:
            raise CustomException(e,sys)

        

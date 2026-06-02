


import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.components.data_ingestion import DataIngetion
from churn.entity.config_entity import DataIngestionConfig
from churn.entity.artifact_entity import DataIngestionArtifact


class TrainingPipeline:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        
        self.data_ingestion_config = data_ingestion_config
    
    def start_data_ingestion(self)->DataIngestionArtifact:

        try:

            logger.info("Entered into  start_data_ingestion function in training pipeline class ")

            data_ingestion_obj = DataIngetion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion_obj.initiate_data_ingetion()

            return data_ingestion_artifact
        

        except Exception as e:

            raise CustomException(e,sys)
    
    def run_pipeline(self):


        try:

            logger.info("Entered into run pipeline ")

            data_ingestion_artifact = self.start_data_ingestion()

        

        
        except Exception as e:
            raise CustomException(e,sys)
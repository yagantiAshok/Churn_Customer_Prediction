


import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.components.data_ingestion import DataIngetion
from churn.components.data_validation import DataValidation

from churn.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig)

from churn.entity.artifact_entity import (DataIngestionArtifact,
                                          DataValidationArtifact)
                                          


class TrainingPipeline:

    def __init__(self,data_ingestion_config:DataIngestionConfig, 
                      data_validation_config:DataValidationConfig):
        
        self.data_ingestion_config = data_ingestion_config
        self.data_validation_config = data_validation_config
    
    def start_data_ingestion(self)->DataIngestionArtifact:

        try:

            logger.info("Entered into  start_data_ingestion function in training pipeline class ")

            data_ingestion_obj = DataIngetion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion_obj.initiate_data_ingetion()

            return data_ingestion_artifact
        

        except Exception as e:

            raise CustomException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:

        try:

            logger.info("Entered into start dat validation function")

            data_validation_obj  = DataValidation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifact)

            data_validation_artifact = data_validation_obj.initiate_data_validation()

            return data_validation_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipeline(self):

        try:

            logger.info("Entered into run pipeline ")

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

        
        except Exception as e:
            raise CustomException(e,sys)
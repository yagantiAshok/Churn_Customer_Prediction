


import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.components.data_ingestion import DataIngetion
from churn.components.data_validation import DataValidation
from churn.components.data_transformation import DataTransformation

from churn.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig)

from churn.entity.artifact_entity import (DataIngestionArtifact,
                                          DataValidationArtifact,
                                          DataTransformationArtifact)
                                          


class TrainingPipeline:

    def __init__(self,data_ingestion_config:DataIngestionConfig, 
                      data_validation_config:DataValidationConfig,
                      data_transformation_config:DataTransformationConfig):
        
        self.data_ingestion_config = data_ingestion_config
        self.data_validation_config = data_validation_config
        self.data_transformation_config = data_transformation_config
    
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
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact)->DataTransformationArtifact:

        try:

            logger.info("Entered into start data transformation function")

            data_transformation_obj = DataTransformation(data_transformation_config=self.data_transformation_config,data_ingetion_artifcat=data_ingestion_artifact )

            data_transformation_artifact = data_transformation_obj.initiate_data_transformation()

            return data_transformation_artifact
        

        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipeline(self):

        try:

            logger.info("Entered into run pipeline ")

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            if not data_validation_artifact.validation_status:
                
                return f"Data validation Status {data_validation_artifact.validation_status}"
            

            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)

        
        except Exception as e:
            raise CustomException(e,sys)
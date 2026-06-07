


import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.components.data_ingestion import DataIngetion
from churn.components.data_validation import DataValidation
from churn.components.data_transformation import DataTransformation
from churn.components.model_training import ModelTrainer
from churn.components.model_evaluation import ModelEvaluation
from churn.components.model_pusher import ModelPusher

from churn.entity.config_entity import (DataIngestionConfig,
                                        DataValidationConfig,
                                        DataTransformationConfig
                                        ,ModelTrainerConfig,
                                        ModelEvaluationConfig,
                                        ModelPusherConfig)

from churn.entity.artifact_entity import (DataIngestionArtifact,
                                          DataValidationArtifact,
                                          DataTransformationArtifact,
                                          ModelTrainerArtifcat,
                                          ModelEvaluationArtifact,
                                          ModelPusherArtifact)
                                          


class TrainingPipeline:

    def __init__(self,data_ingestion_config:DataIngestionConfig, 
                      data_validation_config:DataValidationConfig,
                      data_transformation_config:DataTransformationConfig,
                      Model_trainer_config:ModelTrainerConfig,
                      model_evaluation_config:ModelEvaluationConfig,
                      model_pusher_config:ModelPusherConfig):
        
        self.data_ingestion_config = data_ingestion_config
        self.data_validation_config = data_validation_config
        self.data_transformation_config = data_transformation_config
        self.model_trainer_config = Model_trainer_config
        self.model_evaluation_config = model_evaluation_config
        self.model_pusher_config = model_pusher_config
    
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
    

    def start_model_trainer(self,data_transfromation_artifcat)->ModelTrainerArtifcat:

        try:

            logger.info("Entered into start model trainer")

            model_trainer_obj = ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifcat=data_transfromation_artifcat)

            model_trainer_artifcat = model_trainer_obj.initiate_model_training()

            return model_trainer_artifcat

        
        except Exception as e:

            raise CustomException(e,sys)
    
    def start_model_evaluation(self,data_ingestion_artifcat:DataIngestionArtifact,model_trainer_artifcat:ModelTrainerArtifcat)->ModelEvaluationArtifact:


        try:
            logger.info("Entered into start model evaluation function")

            model_evaluation_obj = ModelEvaluation(model_evaluation_config=self.model_evaluation_config,data_ingestion_artifact=data_ingestion_artifcat,model_trainer_artifact=model_trainer_artifcat)

            evaluation_artifcat = model_evaluation_obj.initiate_model_evaluation()

            return evaluation_artifcat
        
        except Exception as e:

            raise CustomException(e,sys)
    
    def start_model_pusher(self,model_evaluation_artifcat:ModelEvaluationArtifact)->ModelPusherArtifact:

        try:

            logger.info("Entered into start model_pusher function")

            model_pusher_obj = ModelPusher(model_pusher_config=self.model_pusher_config,model_evalutaion_artifact=model_evaluation_artifcat)

            return model_pusher_obj.initiate_model_pusher()

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

            model_trainer_artifcat = self.start_model_trainer(data_transfromation_artifcat=data_transformation_artifact)

            model_evaluation_artifcat = self.start_model_evaluation(data_ingestion_artifcat=data_ingestion_artifact,model_trainer_artifcat=model_trainer_artifcat)

            if  not model_evaluation_artifcat.is_model_accepeted:

                return f"Model Is not Accepted"

            model_evaluation_artifact = self.start_model_pusher(model_evaluation_artifcat=model_evaluation_artifcat)
            


        
        except Exception as e:
            raise CustomException(e,sys)
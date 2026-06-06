

import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.s3_estimator import s3estimator
from churn.entity.estimator import churnmodel
from churn.entity.config_entity import ModelEvaluationConfig
from churn.entity.artifact_entity import ModelEvaluationArtifact,DataIngestionArtifact,ModelTrainerArtifcat
import pandas as pd
from churn.constants import TARGET_COLUMN
from dataclasses import dataclass
from sklearn.metrics import f1_score

@dataclass
class EvaluatedModelReponse:

    trained_model_f1_score:float
    best_model_f1_score:float
    is_model_accepted:bool
    difference:float

class ModelEvaluation:

    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                      model_trainer_artifact:ModelTrainerArtifcat,
                      data_ingestion_artifact:DataIngestionArtifact):
        
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifcat = model_trainer_artifact
        self.data_ingestion_artifcat = data_ingestion_artifact
    
    def get_best_model(self):

        try:

            bucket_name = self.model_evaluation_config.s3_bucket_name
            model_path = self.model_evaluation_config.s3_model_key_path

            s3_estimator = s3estimator(
                bucket_name=bucket_name,model_path=model_path
            )

            model = s3_estimator.is_model_present()

            if model is None:

                return None
            
            logger.info(" No Model is  There in s3 bucket ")
            
            return model

        except Exception as e:

            raise CustomException(e,sys)
    
    def evaluate_model(self):

        try:

            test_data = pd.read_csv(self.data_ingestion_artifcat.test_file_path)

            test_data["TotalCharges"] = pd.to_numeric(test_data["TotalCharges"], errors="coerce")
            test_data.dropna(subset=["TotalCharges"], inplace=True)

            y = test_data[TARGET_COLUMN]

            x =  test_data.drop(TARGET_COLUMN,axis=1)

            map_dict = {"No": 0, "Yes": 1}

            y = y.map(map_dict)

            trained_model_f1_score = self.model_trainer_artifcat.fl_score

            best_model_f1_score = 0

            best_model = self.get_best_model()

            if best_model is not None:

                y_hat_best_model = best_model.predict(x)

                best_model_f1_score = f1_score(y,y_hat_best_model)
            
            

            result = EvaluatedModelReponse(trained_model_f1_score= trained_model_f1_score,
                            best_model_f1_score=best_model_f1_score,
                            is_model_accepted= trained_model_f1_score > best_model_f1_score,
                            difference = trained_model_f1_score - best_model_f1_score)
                        
            logger.info(f"Result: {result}")

            return result

    
        except Exception as e:
            
            raise CustomException(e,sys)
    


    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

        try:

            logger.info("Entered into initaite model evaluation")

            result  = self.evaluate_model()

            model_evaluation_artifcat = ModelEvaluationArtifact(

                is_model_accepeted= result.is_model_accepted,
                s3_model_path= self.model_evaluation_config.s3_model_key_path,
                trained_model_path= self.model_trainer_artifcat.model_trained_obj_path,
                changed_accuracy=result.difference
            )


            return model_evaluation_artifcat


        except Exception as e:

            raise CustomException(e,sys)


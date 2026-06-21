
import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.config_entity import ModelTrainerConfig
from churn.entity.artifact_entity import ModelTrainerArtifcat,DataTransformationArtifact
import pandas as pd
from churn.utils.main_utils import read_yaml,extract_data_from_nuumpy,save_obj,load_obj
from churn.entity.estimator import churnmodel
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,f1_score,recall_score,precision_score
import numpy as np
from churn.model_registry.models import models
from churn.constants import MODEL_FILE

class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,
                      data_transformation_artifcat:DataTransformationArtifact,
                      model_yaml_file = MODEL_FILE):
        
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifcat = data_transformation_artifcat
        self.model_file = read_yaml(model_yaml_file)
    


    
    def predict(self,y_test,y_pred):

        try:

            logger.info("Entered into predict function In Model Trainer class")

            evaluation_metrics = {

                "accuracy" : accuracy_score(y_test,y_pred),
                "f1":    f1_score(y_test,y_pred),
                "recall": recall_score(y_test,y_pred),
                "precision": precision_score(y_test,y_pred)

            }

            logger.info(f"test accuracy and recall {evaluation_metrics['accuracy'],evaluation_metrics['recall']}")

            return evaluation_metrics


        except Exception as e:

            raise CustomException(e,sys)
        
        
    def __split(self,data:np.ndarray):

        try:

            x  = data[:,:-1]

            y  = data[:,-1]

            return x,y

        
        except Exception as e:

            raise CustomException(e,sys)


    
    def Model_Training(self):

        try:

            logger.info("Entered into model training function in model Training")

            train_processed_data = extract_data_from_nuumpy(file_path=self.data_transformation_artifcat.trasformed_train_file_path)

            test_processed_data = extract_data_from_nuumpy(file_path=self.data_transformation_artifcat.transformed_test_file_path)


            # split data of train

            x_train,y_train = self.__split(train_processed_data)

            # split data of test

            x_test,y_test = self.__split(test_processed_data)


            model = models[self.model_file.model_name.model]

            params = self.model_file.model_params

            params_loaded_model = model(**params)

            trained_model = params_loaded_model.fit(x_train,y_train)


            y_pred = trained_model.predict(x_test)

            metrics = self.predict(y_test,y_pred)

            # save model to an object

            preprocessing_obj = load_obj(file_path=self.data_transformation_artifcat.preprocess_file_path)

            churn_model = churnmodel(preprocessing_obj=preprocessing_obj,trained_model_obj=trained_model)

            save_obj(self.model_trainer_config.model_trainer_trained_path,churn_model)


            return metrics


        except Exception as e:

            raise CustomException(e,sys)
    
    def initiate_model_training(self)->ModelTrainerArtifcat:

        try:

            logger.info("Entered innto initiate model training function")

            metrics = self.Model_Training()


            model_trainer_artifact = ModelTrainerArtifcat(

                fl_score= metrics["f1"],
                accuracy_score=metrics["accuracy"],
                recall= metrics["recall"],
                precision=metrics["precision"],
                model_trained_obj_path=self.model_trainer_config.model_trainer_trained_path

                
            )

            return model_trainer_artifact

        except Exception as e:

            raise CustomException(e,sys)



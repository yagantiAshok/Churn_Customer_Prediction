

import sys
import os 
import pandas as pd
import numpy as np
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.config_entity import DataTransformationConfig
from churn.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from churn.constants import SCHEMA_FILE
from churn.utils.main_utils import read_yaml,save_data_to_numpy,save_obj



class DataTransformation:

    def __init__(self, data_transformation_config:DataTransformationConfig,
                      data_ingetion_artifcat:DataIngestionArtifact,
                      schema_file = SCHEMA_FILE):
        
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingetion_artifcat
        self.schema_file = schema_file

        self.schema_data = read_yaml(self.schema_file)

    
    def creating_preprocess_object(self):

        try:

            logger.info("Entered into creating_preprocess_object function in DataTransformation")

            numerical_columns = self.schema_data.numerical_columns
            categorical_columns = self.schema_data.categorical_columns

            numerical_pipeline = Pipeline([

                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

            ])

            categorical_pipeline = Pipeline([
                ("impute",SimpleImputer(strategy="most_frequent")),
                ("scaler",OneHotEncoder(handle_unknown="ignore"))
            ])


            preprocess = ColumnTransformer(transformers=[

                ("numerical_columns",numerical_pipeline,numerical_columns),
                ("categorical_columns",categorical_pipeline,categorical_columns)

            ])

            logger.info("Created object for columnTransformer")


            return preprocess

        

        except Exception as e:
            raise CustomException(e,sys)
        
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:

        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df.dropna(subset=["TotalCharges"], inplace=True)

        # Drop columns 

        df.drop(columns=self.schema_data.drop_column.column, axis=1, inplace=True)
        return df

    def transforming_data(self):

        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            # by using clean method we clean data without repetition

            train_df = self._clean_data(train_df)
            test_df = self._clean_data(test_df)

            # target 

            target = self.schema_data.Target_column.target
            
            # Map target 

            map_dict = {"No": 0, "Yes": 1}

            train_y = train_df[target].map(map_dict)
            test_y = test_df[target].map(map_dict)

            train_x = train_df.drop(columns=[target])
            test_x = test_df.drop(columns=[target])

            # Process Features

            preprocessor = self.creating_preprocess_object()
            train_x_proc = preprocessor.fit_transform(train_x)
            test_x_proc = preprocessor.transform(test_x)

            # Save and Return
            train_arr = np.c_[train_x_proc, np.array(train_y)]
            test_arr = np.c_[test_x_proc, np.array(test_y)]

            save_obj(self.data_transformation_config.data_transformation_processed_file_path, preprocessor)
            save_data_to_numpy(self.data_transformation_config.data_transformation_train_file_path, train_arr)
            save_data_to_numpy(self.data_transformation_config.data_transformation_test_file_path, test_arr)

            logger.info("Data Transformation Completed")

        except Exception as e:
            raise CustomException(e, sys)
            
    def initiate_data_transformation(self)->DataTransformationArtifact:

            try:
                logger.info("Entered Into initiate data transformation function")

                self.transforming_data()

                data_transformation_artifact = DataTransformationArtifact(

                    preprocess_file_path= self.data_transformation_config.data_transformation_processed_file_path,

                    trasformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path,

                    transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path

                )

                return data_transformation_artifact

            except Exception as e:

                raise CustomException(e,sys)
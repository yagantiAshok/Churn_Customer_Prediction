

import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.config_entity import DataValidationConfig
from churn.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from churn.constants import  SCHEMA_FILE
import pandas as pd 
from churn.utils.main_utils import read_yaml,create_folder_path,write_yaml


from evidently.report import Report 
from evidently.metric_preset import DataDriftPreset

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                      data_ingestion_artifact:DataIngestionArtifact,
                      Schema_file = SCHEMA_FILE):
        
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifcat = data_ingestion_artifact
        self.schema_file = Schema_file

        self.schema_data = read_yaml(self.schema_file)
        
    
    def checking_validation_status(self):

        try:



            logger.info("Entered into checking validation status function")

            test_data = pd.read_csv(self.data_ingestion_artifcat.test_file_path)

            actual_columns = list(test_data.columns)

            expected_columns = list(self.schema_data.trainset_columns.keys())

            excepted_numerical_columns = self.schema_data.numerical_columns

            excepted_categorical_columns = self.schema_data.categorical_columns

            error_messages = []

            validation_status = True

            """
            1. CHECKING MISSING COLUMNS

            """

            missing_columns = []

            for column in expected_columns:

                if column not in actual_columns:

                    missing_columns.append(column)

                
            if len(missing_columns)>0:

                validation_status = False

                error_messages.append(
                    f"Missing columns are : {missing_columns}"
                )
            
            logger.info(f"missing columns are : {missing_columns}")

            """
            2.CHECKING EXTRA COLUMNS 

            """

            extra_columns = []

            for column in extra_columns:

                if column not in expected_columns:

                    extra_columns.append(column)
            
            if len(extra_columns)>0:

                validation_status =  False

                error_messages.append(
                    f"Extra columns are : {extra_columns}"
                )

            logger.info(f"Extra columns are : {extra_columns}")


            """
            3.CHECKING SCHEMA OF AN DATA

            """

            missing_data_types = []

            for column, expected_data_type in self.schema_data.trainset_columns.items():

                if column in actual_columns:

                    actual_type = test_data[column].dtype

                    if actual_type!=expected_data_type:

                        missing_data_types.append(
                            {
                                "actual Column":column,
                                "actual_type":actual_type,
                                "expected_type":expected_data_type
                            }
                        )
            
            if len(missing_data_types)>0:

                validation_status = False

                error_messages.append(
                    f"Schame not matching columns are : {missing_data_types}"
                )

            logger.info(f"schema not matching columns : {missing_data_types}")
            
            """
            4.CHECKING NUMERICAL COLUMNS

            """

            missing_num_columns = []

            for column in excepted_numerical_columns:

                if column not in actual_columns:

                    missing_num_columns.append(missing_num_columns)
            
            if len(missing_num_columns)>0:

                error_messages.append(
                    f"Missing Numerical columns are : {missing_num_columns}"
                )
            
            logger.info(f"Missing Num columns : {missing_num_columns}")
        
            
            """
            5.CHECKING CATEGORIVAL COLUMNS
            
            """

            missing_cat_columns = []

            for  column in excepted_categorical_columns:

                if column not in actual_columns:

                    missing_cat_columns.append(column)
            
            if len(missing_cat_columns)>0:

                error_messages.append(
                    f"Missing cat columsn : {missing_cat_columns}"
                )
            
            logger.info(f"Missing cat columns : {missing_cat_columns}")


            """
            6. DUPLICATE ROWS VALIDATION

            """

            duplicate_rows = test_data.duplicated().sum()

            if duplicate_rows > 0:

                error_messages.append(
                    f"Test data has duplicated rows : {duplicate_rows}"
                )

            logger.info(f"duplicate rows present : {duplicate_rows}")

            """

            7. CHECKING NAN PERCENTAGE

            """

            nan_columns = []

            for column in actual_columns:

                ratio = test_data[column].isnull().mean()*100

                if ratio > 0:

                    nan_columns.append(
                        {
                            "Column" :column,
                            "nan_ratio": ratio
                        }
                    )
            
            if len(nan_columns) > 0:

                error_messages.append(
                    f"nan columns are : {nan_columns}"

                )
            
            logger.info(f"Nan columns : {nan_columns}")


            # now create path for validation to store

            create_folder_path(self.data_validation_config.data_validation_status_file)

            with open(self.data_validation_config.data_validation_status_file,"w") as file:

                file.write(f"Validation_status :  { validation_status}\n\n")

                for message in error_messages:

                    file.write(message + "\n")
        
            logger.info(f"Validation status :  {validation_status}")
            
            return validation_status


        except Exception as e:

            raise CustomException(e,sys)
    
    def checking_data_drift(self):
        
        try:

            logger.info("Entered into checking data drift fucction")

            train_data = pd.read_csv(self.data_ingestion_artifcat.train_file_path)
            test_data = pd.read_csv(self.data_ingestion_artifcat.test_file_path)


            report = Report(metrics=[DataDriftPreset()])

            report.run(
                reference_data=train_data,
                current_data=test_data
            )

            report_dict = report.as_dict()

            logger.info(f"Data Drift report generated {report_dict}")

            drift_status = report_dict["metrics"][0]["result"]["dataset_drift"]

            drifted_columns = report_dict["metrics"][0]["result"].get("drift_by_features","NOT THERE ")

            no_of_drifted_columns = report_dict["metrics"][0]["result"]["number_of_drifted_columns"]
            no_of_columns = report_dict["metrics"][0]["result"]["number_of_columns"]

            drift_dict= {

                "DRIFT_STATUS": drift_status,
                "No_of_drifted_columns":no_of_drifted_columns,
                "No_of_columns":no_of_columns,
                "DRIFTED_COLUMNS": drifted_columns

            }


            write_yaml(self.data_validation_config.data_validation_drift_report_file,drift_dict)

            return drift_status



        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        
        try:
            logger.info("Entered into initiate data validation Function")

            validation_status = self.checking_validation_status()

            drift_status = self.checking_data_drift()

            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                drft_status= drift_status,
                drift_report_file_path=self.data_validation_config.data_validation_drift_report_file
            )
           
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e,sys)
    


    

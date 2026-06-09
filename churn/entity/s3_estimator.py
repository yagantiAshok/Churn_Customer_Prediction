


import sys
from churn.exception import CustomException
from churn.logger import logger
from churn.cloud_storage.aws_storage import SimpleStorageService
from churn.entity.estimator import churnmodel

from pandas import DataFrame

class s3estimator:

    def __init__(self,bucket_name,model_path):

        print("s3_estimator_id",id(self))
        print()
        

        self.service = SimpleStorageService()

        self.bucket_name = bucket_name

        self.model_path =  model_path

        self.loaded_model :churnmodel = None
    

    def is_model_present(self):

        try:

            return self.service.is_key_path_avialble(bucket_name=self.bucket_name,s3_key=self.model_path)

        
        except Exception as e:

            raise CustomException(e,sys)
    
    def load_model(self):

        try :

            return self.service.load_model(bucket_name=self.bucket_name,model_name=self.model_path)

        
        except Exception as e:

            raise CustomException(e,sys)
        
    
    def savemodel(self,from_file,to_filename):

        try:

            return self.service.upload_file(from_filename=from_file,bucket_name=self.bucket_name,to_filename=to_filename)

        
        except Exception as e:

            raise CustomException(e,sys)
    
    def predict(self,data:DataFrame):

        try:

            if self.loaded_model is None:

                self.loaded_model = self.load_model()
            
            return self.loaded_model.predict(data)
        

        except Exception as e:

            raise CustomException(e,sys)
        
        

    


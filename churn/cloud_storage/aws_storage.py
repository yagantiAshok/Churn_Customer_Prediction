
import boto3
from churn.exception import CustomException
from churn.logger import logger
import sys
from churn.externel_connections.connection import s3Client
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket
from io import StringIO
import os 
import joblib



class SimpleStorageService:

    def __init__(self):
        
        self.s3 = s3Client()
        self.resources : boto3.resource = self.s3.resources
        self.client : boto3.client = self.s3.client
    
    def is_s3_key_path_available_single_file(self,bucket_name,s3_key):

        try:

            objects = self.client.list_objects_v2(Bucket = bucket_name) #self.client.head_object(Bucket=bucket_name, Key=s3_key)

            file = [ obj["Key"] for obj in objects["Contents"] if obj["Key"]==s3_key] 

            if len(file)>0:

                return True
            
            return False

        except Exception as e:

            raise CustomException(e,sys)
    
    def get_bucket(self,bucket_name):

        try:

            logger.info("entered into get bucket function")

            bucket = self.resources.Bucket(bucket_name)

            logger.info("Got The Bucket")

            return bucket

        
        except Exception as e:

            raise CustomException(e,sys)
        
    def is_key_path_avialble(self,bucket_name,s3_key):

        try:

            bucket = self.get_bucket(bucket_name)

            files = [file_object for file_object in bucket.objects.filter(Prefix = s3_key)]

            if len(files)>0:

                return True
            
            logger.info("S3 key path not avialble")

            return None

        
        except Exception as e:

            raise CustomException(e,sys)
        
    @staticmethod
    def read_object(object_name: str, decode:bool =True, make_readable:bool =False):

        try:

            logger.info("Entered into read object method")

            fun = (
                lambda: object_name.get()['Body'].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )

            conv_fun = lambda: StringIO(fun()) if make_readable is True else fun()

            return conv_fun()

        except Exception as e:

            raise CustomException(e,sys)
        
    def get_file_object(self, filename: str, bucket_name:str):

        try:

            logger.info("Entered into get file object method")

            bucket =self.get_bucket(bucket_name)

            file_objects = [ file_object for file_object in bucket.objects.filter(Prefix=filename)]

            func = lambda x: x[0] if len(x) == 1 else x

            file_object = func(file_objects)

            return file_object

        except Exception as e:
            raise CustomException(e,sys)



    def load_model(self, model_name:str,bucket_name:str ,model_dir :str = None)->object:

        try:
            logger.info("Entered in to load model function in simple storage service")
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )

            model_file = func()

            file_object = self.get_file_object(model_file,bucket_name)
            model_obj = self.read_object(file_object,decode = False)
            model = joblib.load(model_obj)

            logger.info("Modle loaded from s3 bucket")

            return model

        except Exception as e:

            raise CustomException(e,sys)
        
        
    def upload_file(self,from_filename: str, to_filename :str,bucket_name:str,remove:bool=False):

        try :

            logger.info("Entered into upload file function (aws bucket)")

            logger.info(f"uploading  {from_filename} file to {to_filename} bucket ")

            
            self.client.upload_file(from_filename,bucket_name,to_filename)

            logger.info("File uploaded into s3 bucket")


            if remove is True:
                os.remove(from_filename)

                logger.info(f"Remove is set to {remove} .deleted the file")
            else:

                logger.info(f"Remove is set to {remove},not deleted")

        except Exception as e:

            raise CustomException(e,sys)
    
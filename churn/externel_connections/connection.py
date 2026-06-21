
import os 
from churn.constants import MONGODB_URI,DATA_BASE_NAME,aws_acces_key,aws_secret_access,region
from churn.logger import logger
from churn.exception import CustomException
import pymongo
import sys
import boto3

import certifi

ca = certifi.where()


class MongoClient:

    client = None

    def __init__(self,data_base=DATA_BASE_NAME):

        try :

            if MongoClient.client is None:

                mongodb_uri = os.getenv(MONGODB_URI)

                if mongodb_uri is None:

                    raise ValueError(f"Envronment variable {MONGODB_URI} not exists")
                

                MongoClient.client = pymongo.MongoClient(mongodb_uri,tlsCAFile=ca)

                MongoClient.client.admin.command("ping")

                logger.info("MomgoDb Connection successfully Established")
            
            self.database = MongoClient.client[data_base]
            
            self.client = MongoClient.client

            logger.info(f"MongoDb Connection success ")
        
        except Exception as e:

            logger.info("MongoDb initiiztaion failed")
            
            raise CustomException(e,sys)
        
class s3Client:

    client = None
    resources = None

    def __init__(self,REGION_NAME = region):

        if s3Client.client is None or s3Client.resources is None:

            __acces_key_id = os.getenv(aws_acces_key)
            __secret_access_key = os.getenv(aws_secret_access)

            if __acces_key_id is None:

                raise Exception(f"access key if not found {__acces_key_id} in system")
            
            if __secret_access_key is None:

                raise Exception(f"secret access key id not found {__secret_access_key} in system")
            
            s3Client.client = boto3.client("s3",
                                            aws_access_key_id = __acces_key_id,
                                            aws_secret_access_key = __secret_access_key,
                                            region_name = REGION_NAME)
            
            s3Client.resources = boto3.resource("s3",
                                            aws_access_key_id = __acces_key_id,
                                            aws_secret_access_key = __secret_access_key,
                                            region_name = REGION_NAME)
        
        self.resources = s3Client.resources
        self.client = s3Client.client

            



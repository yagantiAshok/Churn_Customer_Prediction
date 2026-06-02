
import os 
from churn.constants import MONGODB_URI,DATA_BASE_NAME
from churn.logger import logger
from churn.exception import CustomException
import pymongo
import sys


class MOngoclient:

    client = None

    def __init__(self,data_base=DATA_BASE_NAME):

        try :

            if MOngoclient.client is None:

                mongodb_uri = os.getenv(MONGODB_URI)

                if mongodb_uri is None:

                    raise Exception({f"Envronment variable not exists: {MONGODB_URI}"})
                
                client = pymongo.MongoClient(mongodb_uri)

                MOngoclient.client = client
            
            self.database = client[data_base]
            
            self.client = client

            logger.info(f"MongoDb Connection success ")
        
        except Exception as e:
            
            raise CustomException(e,sys)



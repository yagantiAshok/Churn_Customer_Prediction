


import pandas as pd
import sys
from churn.logger import logger
from churn.exception import CustomException
from churn.externel_connections.connection import MongoClient
from typing import Optional


class ChurnData:

    def __init__(self):

        self.mongo_client = MongoClient()
    

    def extract_data_from_mongodb(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:


        try:

            logger.info("Entered into extract_data_from_mongodm function in ChurnData Class")

            if database_name is None:


                collection = self.mongo_client.database[collection_name]
            
            else:

                collection = self.mongo_client.client[database_name][collection_name]
            
            data = list(collection.find())

            if not data:

                logger.warning(f"Collection {collection_name}  is empty ")

                return pd.DataFrame()

            data_frame = pd.DataFrame(data)

            if "_id" in data_frame.columns:

                data_frame.drop(columns=["_id"],inplace  = True)

            logger.info(f"MomgoDb Data converted into DataFrame {data_frame.shape}")
            
            return data_frame
        

        except Exception as e:
            raise CustomException(e,sys)

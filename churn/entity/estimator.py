

import sys
from churn.logger import logger
from churn.exception import CustomException
from sklearn.pipeline import Pipeline
from pandas import DataFrame


class churnmodel:

    def __init__(self,preprocessing_obj:Pipeline,trained_model_obj: object ):

        self.preprocessing_obj = preprocessing_obj

        self.trainded_model_obj = trained_model_obj

    def predict(self,Dataframe :DataFrame):

        try :
            logger.info("Entered into predict fundtion inside visamodel")

            transformed_features = self.preprocessing_obj.transform(Dataframe)

            logger.info("Transformed raw features into machine language")

            return self.trainded_model_obj.predict(transformed_features)

        except Exception as e:
            raise CustomException(e,sys)


        
        

import sys 
from churn.constants import BUCKET_NAME,MODEL_FILE_NAME
from churn.logger import logger
from churn.exception import CustomException
from churn.entity.s3_estimator import s3estimator
import pandas as pd


class CustomerData:

    def __init__(
        self,
        gender,
        SeniorCitizen,
        Partner,
        Dependents,
        tenure,
        PhoneService,
        MultipleLines,
        InternetService,
        OnlineSecurity,
        OnlineBackup,
        DeviceProtection,
        TechSupport,
        StreamingTV,
        StreamingMovies,
        Contract,
        PaperlessBilling,
        PaymentMethod,
        MonthlyCharges,
        TotalCharges
    ):

        self.gender = gender
        self.SeniorCitizen = SeniorCitizen
        self.Partner = Partner
        self.Dependents = Dependents
        self.tenure = tenure
        self.PhoneService = PhoneService
        self.MultipleLines = MultipleLines
        self.InternetService = InternetService
        self.OnlineSecurity = OnlineSecurity
        self.OnlineBackup = OnlineBackup
        self.DeviceProtection = DeviceProtection
        self.TechSupport = TechSupport
        self.StreamingTV = StreamingTV
        self.StreamingMovies = StreamingMovies
        self.Contract = Contract
        self.PaperlessBilling = PaperlessBilling
        self.PaymentMethod = PaymentMethod
        self.MonthlyCharges = MonthlyCharges
        self.TotalCharges = TotalCharges

    def get_customer_data_as_dict(self):

        input_data = {
            "gender": self.gender,
            "SeniorCitizen": self.SeniorCitizen,
            "Partner": self.Partner,
            "Dependents": self.Dependents,
            "tenure": self.tenure,
            "PhoneService": self.PhoneService,
            "MultipleLines": self.MultipleLines,
            "InternetService": self.InternetService,
            "OnlineSecurity": self.OnlineSecurity,
            "OnlineBackup": self.OnlineBackup,
            "DeviceProtection": self.DeviceProtection,
            "TechSupport": self.TechSupport,
            "StreamingTV": self.StreamingTV,
            "StreamingMovies": self.StreamingMovies,
            "Contract": self.Contract,
            "PaperlessBilling": self.PaperlessBilling,
            "PaymentMethod": self.PaymentMethod,
            "MonthlyCharges": self.MonthlyCharges,
            "TotalCharges": self.TotalCharges
        }

        return input_data
    
    def convert_customer_data_todataframe(self)->pd.DataFrame:

        try:
            logger.info("Entered into conversion data into dataframe")

            data = self.get_customer_data_as_dict()

            data_frame = pd.DataFrame([data])

            return data_frame
        

        except Exception as e:
            raise CustomerData(e,sys)
    

class ChurnClassifier:

    def __init__(self,bucket_name = BUCKET_NAME,model_key_path = MODEL_FILE_NAME):
        
        self.bucket_name = bucket_name
        self.model_key_path = model_key_path

        logger.info("loading model")

    
    def predict(self,data_frame:pd.DataFrame):

        try:

            logger.info("Entered into predict function")


            s3_estimator = s3estimator(bucket_name=self.bucket_name,model_path=self.model_key_path)

            churn_class = s3_estimator.predict(data=data_frame)

            return churn_class
        

        except Exception as e:

            raise CustomException(e,sys)

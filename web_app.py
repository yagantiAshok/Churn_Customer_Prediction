


from churn.pipeline.predicting_pipeline import CustomerData,ChurnClassifier
from churn.logger import logger
from churn.exception import CustomException
import streamlit as st

from churn.utils.main_utils import read_yaml
from churn.constants import SCHEMA_FILE

data = read_yaml(SCHEMA_FILE)




import streamlit as st

st.set_page_config("Churn Prediction",layout="centered")

st.title("Customer Churn Prediction")


user_data = {}

for field, options in data.fields.items():

    user_data[field] = st.selectbox(field, options)

user_data["tenure"] = st.number_input(
    "tenure",
    min_value=0,
    value=0
)

user_data["MonthlyCharges"] = st.number_input(
    "MonthlyCharges",
    min_value=0.0,
    value=0.0
)

user_data["TotalCharges"] = st.number_input(
    "TotalCharges",
    min_value=0.0,
    value=0.0
)


customer_data = CustomerData(**user_data)

data_frame = customer_data.convert_customer_data_todataframe()

prediction = ChurnClassifier()

pred = prediction.predict(data_frame=data_frame)[0]

if st.button("Predict"):



    if pred==1:

        st.success("Customer is Churn")
    
    else:

        st.error("Cutomer is not churn ")
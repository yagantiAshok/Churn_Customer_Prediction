



# import os 

# path = "ashok"

# print(os.path.dirname(path))

# print(os.path.getsize("notebook/app.py"))
# import sys

# from churn.logger import logger

# from churn.exception import CustomException

# logger.info("Exception handling")

# try:

#     a = 1

#     b = 0

#     print(a/b)

# except Exception as e:
#     raise CustomException(e,sys)

# from pathlib import Path
# import os 

# path = os.path.join("config","schema.yaml")

# from churn.utils.main_utils import read_yaml

# data = read_yaml(path)

# # print(data["trainset_columns"].keys())
# # print(data["trainset_columns"].values())

# # for column ,type_ in data["trainset_columns"].items():

# #     print(column,type_)

# print(data.trainset_columns)


# class student:

#     def __init__(self,name,age):
       
#        self.name = name
#        self.age = age


# obj1 = student(name="ashok",age=8)


# joblib.dump(obj1,filename="custom.pkl")
import streamlit as st

import os 
from churn.utils.main_utils import read_yaml

path = os.path.join("config","schema.yaml")

data  = read_yaml(path)

user_data = {}

for col, items in data.fields.items():

    user_data[col]=st.selectbox(col,items)

if st.button("predict"):

    st.write(user_data)



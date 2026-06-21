



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
# import streamlit as st

# import os 
# from churn.utils.main_utils import read_yaml

# path = os.path.join("config","schema.yaml")

# data  = read_yaml(path)

# user_data = {}

# for col, items in data.fields.items():

#     user_data[col]=st.selectbox(col,items)

# if st.button("predict"):

#     st.write(user_data)


# class st:
    
#     def __init__(self,age):

#         self.name = None

#         self.age = age

# ob1 = st(age=67)

# ob1.name = "ashok"

# print(ob1.age,ob1.name)

# ob = ob1

# print(ob.age,ob.name)

# a = [1,2,3]

# print(a)

# a = [0,2,2]

# print(a)


# class student:

#     data = None

#     def __init__(self,name="ashok"):
        
#         if student.data is None:

#             student.data = name

#             self.name = name

# obj = student()

# print(obj.__dict__)

# print(obj.data)

# obj1 = student()

# print(obj1.__dict__)

# print(obj1.data)

# class Student:

#     data = None

#     def __init__(self):

#         if Student.data is None:

#             data = "ashok"

#             Student.data = data

#         print(data)

# obj = Student()

# obj1 = Student()

# from churn.constants import SCHEMA_FILE

# from churn.utils.main_utils import read_yaml
# import os 

# data = read_yaml(os.path.join("config\model.yaml"))

# model = data.model_name

# print(model.model)

# params = data.model_params

# print(params)

# from setup import models

# print(len(models))

# print(models.values())


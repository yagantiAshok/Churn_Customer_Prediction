
from testing import student

import joblib

data  :student = joblib.load("custom.pkl")

print(data.name)
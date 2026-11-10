
from copy import deepcopy
from fast import app , get_predictor
from fastapi.testclient import TestClient
import pytest

VALID_CUSTOMER = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "Yes",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "One year",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "tenure": 24,
    "MonthlyCharges": 75.5,
    "TotalCharges": 1812.0,
}

class Fakepredictor:

    def __init__(self,prediction = 1, failure = None):
        self.prediction = prediction
        self.failure = failure
        self.calls = 0
        self.last_input = None

    def predict(self,data_frame):
        self.calls += 1
        self.last_input = data_frame.copy()
        if self.failure is not None:
            raise self.failure
        return [self.prediction]

@pytest.fixture
def valid_cutomer():
    return deepcopy(VALID_CUSTOMER)

@pytest.fixture
def fake_predictor():
    return Fakepredictor()

@pytest.fixture
def client(fake_predictor):

    app.dependency_overrides[get_predictor] = lambda :fake_predictor
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_predictor,None)
        
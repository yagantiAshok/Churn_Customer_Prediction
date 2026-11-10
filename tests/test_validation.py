

import pytest
from tests.conftest import VALID_CUSTOMER

@pytest.mark.parametrize("field_value",list(VALID_CUSTOMER.keys()))
def test_every_field_is_required(client,fake_predictor,valid_cutomer,field_value):

    del valid_cutomer[field_value]
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 422
    assert fake_predictor.calls == 0

INVALID_CATEGORY_VALUES = [
    ("gender", "Unknown"),
    ("SeniorCitizen", 2),
    ("Partner", "Maybe"),
    ("Dependents", "Maybe"),
    ("PhoneService", "Maybe"),
    ("MultipleLines", "Maybe"),
    ("InternetService", "Satellite"),
    ("OnlineSecurity", "Maybe"),
    ("OnlineBackup", "Maybe"),
    ("DeviceProtection", "Maybe"),
    ("TechSupport", "Maybe"),
    ("StreamingTV", "Maybe"),
    ("StreamingMovies", "Maybe"),
    ("Contract", "Weekly"),
    ("PaperlessBilling", "Maybe"),
    ("PaymentMethod", "Cash"),
]

@pytest.mark.parametrize("column,invalid_input",INVALID_CATEGORY_VALUES)
def test_is_invalid_input_raises_error(client,fake_predictor,valid_cutomer,column,invalid_input):

    valid_cutomer[column] = invalid_input
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 422
    assert fake_predictor.calls == 0

@pytest.mark.parametrize("field", ["tenure", "MonthlyCharges", "TotalCharges"])
def test_is_negative_numbers_accept(client,fake_predictor,valid_cutomer,field):

    valid_cutomer[field] = -1
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 422
    assert fake_predictor.calls == 0

def test_inavlid_request_has_useful_error_structure(client,valid_cutomer):

    valid_cutomer["gender"] = "unknown"
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 422
    body = response.json()
    assert isinstance(body["detail"],list)
    assert any("gender" in error.get("loc",[]) for error in body["detail"])



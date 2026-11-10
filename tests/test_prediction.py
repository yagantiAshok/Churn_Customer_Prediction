

import pandas as pd
import pytest

@pytest.mark.parametrize(
      "output,expected_message",
    [
        (1,"Customer will churn"),
        (0,"Customer will not churn")
    ],

)

def test_prediction_outcomes(client,fake_predictor,valid_cutomer,output,expected_message):

    fake_predictor.prediction = output
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 200
    assert response.json() == {"prediction":output,"result":expected_message}
    assert fake_predictor.calls == 1

def test_cutomer_data_frame(client,fake_predictor,valid_cutomer):

    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 200
    data_frame = fake_predictor.last_input
    assert isinstance(data_frame,pd.DataFrame)
    assert data_frame.shape[0] == 1
    assert set(data_frame.columns) == set(valid_cutomer.keys())


def test_two_request_calls_predictor_twice(client,valid_cutomer,fake_predictor):

    first = client.post("/predict",json=valid_cutomer)
    second = client.post("/predict",json=valid_cutomer)
    assert first.status_code == 200
    assert second.status_code == 200
    assert fake_predictor.calls == 2

def test_is_numerical_values_accepted(client,valid_cutomer):

    valid_cutomer.update(tenure=0, MonthlyCharges=0.0, TotalCharges=0.0)
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 200


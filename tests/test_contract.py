

def test_is_response_json_for_valid_data(client,valid_cutomer):
    response = client.post("/predict",json=valid_cutomer)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert set(response.json()) == {"prediction","result"}

def test_unknown_url_returns_404(client):
    response = client.get("/home")
    assert response.status_code == 404

def test_get_not_alloed_on_predict(client):
    response = client.get("/predict")
    assert response.status_code == 405

def test_openapi_document_prediction_endpoint(client):
    response = client.get("openapi.json")
    assert response.status_code == 200
    api_spec = response.json()
    assert "/predict" in api_spec["paths"]
    assert "post" in api_spec["paths"]["/predict"]
    assert "requestBody" in api_spec["paths"]["/predict"]["post"]
    assert "200" in api_spec["paths"]["/predict"]["post"]["responses"]
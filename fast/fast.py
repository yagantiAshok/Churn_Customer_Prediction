
from functools import lru_cache
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from fastapi import Request
from fastapi import HTTPException,Depends
from churn.logger import logger

from churn.pipeline.predicting_pipeline import (
    CustomerData,
    ChurnClassifier
)


class ChurnRequest(BaseModel):

    gender: Literal["Male"]
    SeniorCitizen: Literal[0, 1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    PhoneService: Literal["Yes", "No"]

    MultipleLines: Literal[
        "Yes", "No", "No phone service"
    ]

    InternetService: Literal["DSL", "Fiber optic", "No"]

    OnlineSecurity: Literal[
        "Yes", "No", "No internet service"
    ]
    OnlineBackup: Literal[
        "Yes", "No", "No internet service"
    ]
    DeviceProtection: Literal[
        "Yes", "No", "No internet service"
    ]
    TechSupport: Literal[
        "Yes", "No", "No internet service"
    ]
    StreamingTV: Literal[
        "Yes", "No", "No internet service"
    ]
    StreamingMovies: Literal[
        "Yes", "No", "No internet service"
    ]

    Contract: Literal[
        "Month-to-month", "One year", "Two year"
    ]

    PaperlessBilling: Literal["Yes", "No"]

    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]

    tenure: int = Field(ge=0)
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)

class Churnresponse(BaseModel):
    prediction :Literal[0,1]
    result : str 



@asynccontextmanager
async def lifespan(app:FastAPI):

    app.state.predictor = ChurnClassifier()
    yield
    app.state.predictor = None

def get_predictor(request:Request):
    return request.app.state.predictor

app = FastAPI(title="Customer Churn Prediction",lifespan=lifespan)

@app.get("/")
def home():
    return {"Welcome To churn prediction page "}


@app.post("/predict",response_model=Churnresponse)
def predict_churn(customer: ChurnRequest, predictor: ChurnClassifier = Depends(get_predictor)):

    user_data = customer.model_dump()
    customer_data = CustomerData(**user_data)
    data_frame = customer_data.convert_customer_data_todataframe()

    try:
        pred = predictor.predict(data_frame=data_frame)[0]
    except Exception:
        logger.exception("Churn Prediction Failed"),
        raise HTTPException(
            status_code=500,
            detail="Temporary issue on server side, please try again later"
        )

    return {
        "prediction": int(pred),
        "result": (
            "Customer will churn"
            if pred == 1
            else "Customer will not churn"
        )
    }




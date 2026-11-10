
import streamlit
from churn.utils.main_utils import read_yaml
from churn.constants import SCHEMA_FILE
import requests

API_URL = "http://127.0.0.1:8000/predict"


st = streamlit
data = read_yaml(SCHEMA_FILE)
st.set_page_config(
    page_title="Churn Prediction",
    layout="centered"
)
st.title("Customer Churn Prediction")

with st.form("churn form "):

    user_data = {}
    for keys , values in data.fields.items():
        user_data[keys] = st.selectbox(keys,values)

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

    submit = st.form_submit_button("predict")

if submit:

    try:
        response = requests.post(
            json=user_data,
            url = API_URL,
            timeout=90
        )

        response.raise_for_status()
        result = response.json()
        prediction = result["prediction"]

        print(prediction)

        if prediction == 1:
            st.warning("Customer is Churn ")
        else:
            st.success("Customer will not churn")


    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")

    except (ValueError, KeyError, TypeError) as e:
        st.error(f"Invalid API response: {e}")

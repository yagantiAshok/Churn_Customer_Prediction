
import streamlit as st 


st.title("Churn Prediction")

name = st.text_input("Enter Name")

age = st.number_input("Enter age ")

# gender = st.selectbox("Gender",["Male","female"])

gender = st.radio("Gender",["male","female"])

if st.button("predict"):

    if age ==10:

        st.success("Yes")
        
    else:

        st.error("no")

    st.write(name,age,gender)
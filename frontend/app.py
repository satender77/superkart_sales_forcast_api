import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_Weight = st.number_input("Product Weight", min_value=2, value=25)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["low sugar", "regular","no sugar"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area", min_value=0.004, value=0.4)
Product_Type = st.selectbox("Product_Type", ["Fruits and Vegetables", "Snack Foods","Frozen Foods","Dairy","Household","Baking Goods","Canned","Health and Hygiene","Meat","Soft Drinks","Breads","Hard Drinks","Others","Starchy Foods","Breakfast","Seafood"])
Product_MRP = st.number_input("Product_MRP",min_value=10, value=300 )
Store_Establishment_Year = st.number_input("Store_Establishment_Year", min_value=1990, value=2020)
Store_Size = st.selectbox("Store_Size", ["Small", "Medium", "Large"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store_Type", ["Supermarket Type1", "Supermarket Type2", "Grocery Store"])
Product_Id_char = st.selectbox("Product_Id_char", ["FD", "NC"])
Store_Age_Years = st.number_input("Store_Age_Years", min_value=1, value=10)
Product_Type_Category = st.selectbox("Product_Type_Category", ["Perishables", "Non Perishables"])


# Convert user input into a DataFrame
input_data = pd.DataFrame({
    'Product_Weight': [Product_Weight],
    'Product_Sugar_Content': [Product_Sugar_Content],
    'Product_Allocated_Area': [Product_Allocated_Area],
    'Product_Type': [Product_Type],
    'Product_MRP': [Product_MRP],
    'Store_Establishment_Year': [Store_Establishment_Year],
    'Store_Size': [Store_Size],
    'Store_Location_City_Type': [Store_Location_City_Type],
    'Store_Type': [Store_Type],
    'Product_Id_char': [Product_Id_char],
    'Store_Age_Years': [Store_Age_Years],
    'Product_Type_Category': [Product_Type_Category]
})

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales (in dollars)']
        st.success(f"Predicted Sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")

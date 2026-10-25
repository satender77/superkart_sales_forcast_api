# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_forcast_api = Flask("Superkart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("backend_files/superkart_model.joblib")

# Define a route for the home page (GET request)
@superkart_sales_forcast_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Prediction API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_forcast_api.post('/v1/predict')
def predict_sales()():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing sales details and returns
    the predicted sales price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type'],
        'Product_Id_char': property_data['Product_Id_char'],
        'Store_Age_Years': property_data['Store_Age_Years'],
        'Product_Type_Category': property_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make sales prediction
    predicted_sales = model.predict(input_data).tolist()
    
    # Return the actual sales
    return jsonify({'Predicted Sales (in dollars)': predicted_sales})

# Define an endpoint for batch prediction (POST request)
@superkart_sales_forcast_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing property details for multiple store
    and returns the predicted sales prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all stores in the DataFrame (get log_prices)
    predicted_sales = model.predict(input_data).tolist()

    # Create a dictionary of predictions with store IDs as keys
    store_ids = input_data['id'].tolist()  # Assuming 'id' is the store ID column
    output_dict = dict(zip(store_ids, predicted_sales))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_forcast_api.run(debug=True)

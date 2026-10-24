# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_forcast_api = Flask("Superkart Sales Predictor")

# Load the trained machine learning model
model = joblib.load("backend_files/superkart_model.joblib")

# Define the exact columns the model pipeline expects
MODEL_FEATURES = [
    'Product_Weight',
    'Product_Sugar_Content',
    'Product_Allocated_Area',
    'Product_Type',
    'Product_MRP',
    'Store_Establishment_Year',
    'Store_Size',
    'Store_Location_City_Type',
    'Store_Type'
]

# Define a route for the home page (GET request)
@superkart_sales_forcast_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the Superkart Sales Prediction API!"

# Define an endpoint for single prediction (POST request)
@superkart_sales_forcast_api.post('/v1/predict')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It filters the incoming payload to ensure only the features
    the model pipeline expects are sent.
    """
    superkart_data = request.get_json()

    # Safeguard against extra inputs by only selecting the 9 required model columns
    sample = {feature: superkart_data.get(feature) for feature in MODEL_FEATURES}

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make sales prediction
    predicted_sales = model.predict(input_data).tolist()

    # Return the sales matched to frontend requirements ("Predicted Sales (in dollars)")
    return jsonify({'Predicted Sales (in dollars)': predicted_sales[0]})

# Define an endpoint for batch prediction (POST request)
@superkart_sales_forcast_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It reads the CSV file, subsets only the required features, and predicts.
    """
    file = request.files['file']
    input_data = pd.read_csv(file)

    # Extract key identifier for return payload mapping if present
    product_ids = []
    if 'Product_Id' in input_data.columns:
        product_ids = input_data['Product_Id'].tolist()
    else:
        product_ids = [f"Row_{i}" for i in range(len(input_data))]

    # Subset DataFrame to only include features expected by the model pipeline
    filtered_input_data = input_data[MODEL_FEATURES]

    # Make predictions using the filtered DataFrame
    predicted_sales = model.predict(filtered_input_data).tolist()

    # Create a dictionary of predictions mapping the identifier to predictions
    output_dict = dict(zip(product_ids, predicted_sales))

    return jsonify(output_dict)

# Run the Flask application if executed directly
if __name__ == '__main__':
  superkart_sales_forcast_api.run(debug=True)

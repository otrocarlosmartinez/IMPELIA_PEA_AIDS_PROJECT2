import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd


def load_models():
    """Load the trained model and transformers."""
    model = joblib.load("models/stacked_model_at_2025-02-02.pkl")
    scaler = joblib.load("models/scaler_at_2025-03-02.pkl")
    poly = joblib.load("models/poly_at_2025-03-02.pkl")
    return model, scaler, poly

# Load models outside UI to avoid reloading on every interaction
model, scaler, poly = load_models()

st.title("Property Price Predictor")

# Process the data to match the reference format with ordered columns
def prepare_input_data(user_input):
    # Convert dictionary to DataFrame (assuming a single input instance)
    input_data = pd.DataFrame([user_input])

    # Add missing computed columns
    input_data["price"] = 0  # Placeholder (not used in predictions)
    input_data["square_meters_price"] = input_data["square_meters"] / input_data["square_meters"].replace(0, 1)

    # One-hot encode categorical features
    real_state_dummies = pd.get_dummies(input_data["real_state"], prefix="real_state")
    neighborhood_dummies = pd.get_dummies(input_data["neighborhood"], prefix="neighborhood")

    # Drop the original categorical columns
    input_data = input_data.drop(columns=["real_state", "neighborhood"])

    # Ensure baseline category is removed
    real_state_dummies = real_state_dummies.drop(columns=["real_state_flat"], errors="ignore")
    neighborhood_dummies = neighborhood_dummies.drop(columns=["neighborhood_Eixample"], errors="ignore")

    # Concat all dataframes
    input_data = pd.concat([input_data, real_state_dummies, neighborhood_dummies], axis=1)

    # Define expected feature order
    expected_columns = [
        'price', 'rooms', 'bathroom', 'lift', 'terrace', 'square_meters',
        'square_meters_price', 'real_state_apartment', 'real_state_attic',
        'real_state_study', 'neighborhood_Ciutat Vella', 'neighborhood_Gràcia',
        'neighborhood_Horta- Guinardo', 'neighborhood_Les Corts',
        'neighborhood_Nou Barris', 'neighborhood_Sant Andreu',
        'neighborhood_Sant Martí', 'neighborhood_Sants-Montjuïc',
        'neighborhood_Sarria-Sant Gervasi'
    ]

    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0  # Assign default value

    # Reorder columns to match model training order
    input_data = input_data[expected_columns]

    return input_data


# Function to make prediction

def predict_price(user_input):
    input_data = prepare_input_data(user_input)
    input_poly = poly.transform(input_data)
    input_scaled = scaler.transform(input_poly)
    prediction = model.predict(input_scaled)
    return np.expm1(prediction)[0]  # Reverse log transformation

# User input form
with st.form(key="property_form"):
    st.subheader("Enter Property Details")
    
    rooms = st.number_input("Rooms", min_value=1, max_value=8, step=1, value=2)
    bathroom = st.number_input("Bathrooms", min_value=1, max_value=4, step=1, value=1)
    square_meters = st.number_input("Square Meters", min_value=10, max_value=500, step=1, value=70)
    lift = st.checkbox("Lift", value=False)
    terrace = st.checkbox("Terrace", value=False)
    real_state = st.selectbox("Real State", ["flat", "attic", "apartment", "study"])
    neighborhood = st.selectbox("Neighborhood", [
        "Eixample", "Horta- Guinardo", "Sant Andreu", "Gràcia", "Ciutat Vella",
        "Sarria-Sant Gervasi", "Les Corts", "Sant Martí", "Sants-Montjuïc", "Nou Barris"
    ])
    
    submit_button = st.form_submit_button("Calculate Price")

# Perform prediction when button is clicked
if submit_button:
    user_input = {
        "rooms": rooms,
        "bathroom": bathroom,
        "lift": int(lift),
        "terrace": int(terrace),
        "square_meters": square_meters,
        "real_state": real_state,
        "neighborhood": neighborhood
    }
 
    predicted_price = predict_price(user_input)
    st.success(f"### Predicted Price: ${predicted_price:,.2f}")

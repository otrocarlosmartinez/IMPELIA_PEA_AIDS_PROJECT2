import streamlit as st
import joblib
import os
import numpy as np
import pandas as pd

# Load models and transformers
models_dir = "models"
model_files = [f for f in os.listdir(models_dir) if f.endswith(".pkl")]

# Load model and transformers
model = joblib.load(os.path.join(models_dir, "stacked_model_at_2025-02-28.pkl"))
scaler = joblib.load(os.path.join(models_dir, "scaler_at_2025-02-28.pkl"))  
poly = joblib.load(os.path.join(models_dir, "poly_at_2025-02-28.pkl"))

# User input
user_input = {
        "rooms": st.number_input("Rooms", min_value=1, max_value=8, step=1),
        "bathroom": st.number_input("Bathroom", min_value=1, max_value=4, step=1),
        "lift": st.checkbox("Lift"),
        "terrace": st.checkbox("Terrace"),
        "square_meters": st.number_input("Square Meters", min_value=10, max_value=500, step=1),
        "real_state": st.selectbox("Real State", ["flat", "attic", "apartment", "study"]),
        "neighborhood": st.selectbox(
            "Neighborhood",
            [
                "Horta- Guinardo", "Sant Andreu", "Gràcia", "Ciutat Vella",
                "Sarria-Sant Gervasi", "Les Corts", "Sant Martí", "Eixample",
                "Sants-Montjuïc", "Nou Barris"
            ]
        )
    }

# Convert user input to DataFrame
input_df = pd.DataFrame([user_input])


# Process the data to match the reference format with ordered columns
def prepare_input_data(input_df):
    # Make a copy to avoid modifying the original
    input_data = input_df.copy()
    
    # One-hot encode real_state with "flat" as baseline
    real_state_dummies = pd.get_dummies(input_data["real_state"], prefix="real_state")
    # Remove the baseline category "flat"
    if "real_state_flat" in real_state_dummies.columns:
        real_state_dummies = real_state_dummies.drop(columns=["real_state_flat"])
    
    # One-hot encode neighborhood with "Eixample" as baseline
    neighborhood_dummies = pd.get_dummies(input_data["neighborhood"], prefix="neighborhood")
    # Remove the baseline category "Eixample"
    if "neighborhood_Eixample" in neighborhood_dummies.columns:
        neighborhood_dummies = neighborhood_dummies.drop(columns=["neighborhood_Eixample"])
    
    # Drop the original categorical columns
    input_data = input_data.drop(columns=["real_state", "neighborhood"])
    
    # Concat all dataframes
    input_data = pd.concat([input_data, real_state_dummies, neighborhood_dummies], axis=1)
    
    # Define the expected column order
    expected_columns = ['price', 'rooms', 'bathroom', 'lift', 'terrace', 'square_meters',
       'square_meters_price', 'real_state_apartment', 'real_state_attic',
       'real_state_study', 'neighborhood_Ciutat Vella', 'neighborhood_Gràcia',
       'neighborhood_Horta- Guinardo', 'neighborhood_Les Corts',
       'neighborhood_Nou Barris', 'neighborhood_Sant Andreu',
       'neighborhood_Sant Martí', 'neighborhood_Sants-Montjuïc',
       'neighborhood_Sarria-Sant Gervasi']
    
    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0
    
    # Reorder columns to match the expected order
    input_data = input_data[expected_columns]
    
    return input_data

# Generate the final input_data dataframe with columns in the expected order
input_data = prepare_input_data(input_df)


# Apply transformations
input_poly = poly.transform(input_data)  # Now feature count should match
input_scaled = scaler.transform(input_poly)

# Make prediction
prediction = model.predict(input_scaled)
predicted_price = np.expm1(prediction)[0]  # Reverse log transformation

# Display results
st.write(f"### Predicted Price: ${predicted_price:,.2f}")
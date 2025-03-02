import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Set page title
st.title("Predictor precios de alquileres en Barcelona")

@st.cache_resource
def load_models():
    model = joblib.load("models/stacked_model_at_2025-03-02.pkl")
    scaler = joblib.load("models/scaler_at_2025-03-02.pkl")  
    poly = joblib.load("models/poly_at_2025-03-02.pkl")
    return model, scaler, poly

model, scaler, poly = load_models()

def prepare_input_data(input_df):
    input_data = input_df.copy()

    # Compute square_meters_price based on the same logic used during training
    #estimated_price_per_sqm = 16.41  # Adjust based on training logic
    #input_data["square_meters_price"] = input_data["square_meters"] * estimated_price_per_sqm

    # One-hot encode categorical features
    real_state_dummies = pd.get_dummies(input_data["real_state"], prefix="real_state")
    neighborhood_dummies = pd.get_dummies(input_data["neighborhood"], prefix="neighborhood")
    
    # Drop original categorical columns and merge encoded data
    input_data = input_data.drop(columns=["real_state", "neighborhood"], errors='ignore')
    input_data = pd.concat([input_data, real_state_dummies, neighborhood_dummies], axis=1)
    
    # Define expected feature columns (excluding 'price')
    expected_columns = [
        'rooms', 'bathroom', 'lift', 'terrace', 'square_meters',
        'real_state_apartment', 'real_state_attic', 'real_state_study',
        'neighborhood_Ciutat Vella', 'neighborhood_Gràcia',
        'neighborhood_Horta- Guinardo', 'neighborhood_Les Corts',
        'neighborhood_Nou Barris', 'neighborhood_Sant Andreu',
        'neighborhood_Sant Martí', 'neighborhood_Sants-Montjuïc',
        'neighborhood_Sarria-Sant Gervasi'
    ]
    
    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0
    
    # Reorder columns to match model expectations
    input_data = input_data[expected_columns]
    
    return input_data

def predict_price(user_input):
    input_df = pd.DataFrame([user_input])
    input_data = prepare_input_data(input_df)
    
    # Ensure correct feature alignment before transformation
    input_poly = poly.transform(input_data)
    input_scaled = scaler.transform(input_poly)
    
    prediction = model.predict(input_scaled)
    return np.expm1(prediction)[0]  # Reverse log transformation

# User input form
with st.form(key="property_form"):
    st.subheader("Detalles de la propiedad")
    col1, col2 = st.columns(2)
    
    with col1:
        rooms = st.number_input("Habitaciones", min_value=1, max_value=8, step=1, value=2)
        bathroom = st.number_input("Baños", min_value=1, max_value=4, step=1, value=1)
        square_meters = st.number_input("Area (m2)", min_value=10, max_value=500, step=1, value=70)
    
    with col2:
        lift = st.checkbox("Ascensor", value=False)
        terrace = st.checkbox("Terraza", value=False)
        real_state = st.selectbox("Tipo de propiedad", ["flat", "attic", "apartment", "study"])
        neighborhood = st.selectbox(
            "Barrio",
            [
                "Eixample", "Horta- Guinardo", "Sant Andreu", "Gràcia", "Ciutat Vella",
                "Sarria-Sant Gervasi", "Les Corts", "Sant Martí", "Sants-Montjuïc", "Nou Barris"
            ]
        )
    
    submit_button = st.form_submit_button(label="Calcular Precio")

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
    st.success(f"### Predicción de precio: ${predicted_price:,.2f}")
    st.info(f"El precio estimado para alquilar un {real_state} {rooms}h/{bathroom}b de {square_meters}m2 en {neighborhood} es ${predicted_price:,.2f}")


    

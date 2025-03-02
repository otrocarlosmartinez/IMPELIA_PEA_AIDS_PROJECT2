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

def generate_facility_text(lift, terrace):
    if lift and terrace:
        return "con ascensor y terraza"
    elif lift:
        return "con ascensor"
    elif terrace:
        return "con terraza"
    else:
        return "sin ascensor ni terraza"

# User input form
with st.form(key="property_form"):
    st.subheader("Detalles de la propiedad")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        real_state = st.selectbox("Tipo de propiedad", ["flat", "attic", "apartment", "study"])
        neighborhood = st.selectbox(
            "Barrio",
            [
                "Eixample", "Horta- Guinardo", "Sant Andreu", "Gràcia", "Ciutat Vella",
                "Sarria-Sant Gervasi", "Les Corts", "Sant Martí", "Sants-Montjuïc", "Nou Barris"
            ]
        )
        square_meters = st.number_input("Area (m2)", min_value=10, max_value=500, step=1, value=70)
        st.markdown("""
        <style>
        .small-font {
            font-size: 0.8em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="small-font">
        <strong>Tipos de Propiedad</strong>
        <ul>
        <li><strong>Study (Estudio)</strong>: Vivienda pequeña de un solo ambiente que combina sala, dormitorio y cocina, con baño separado. Ideal para individuos o parejas que buscan un espacio compacto.</li>
        <li><strong>Attic (Ático)</strong>: Apartamento en la última planta, con techos inclinados y, a veces, terraza. Su tamaño varía, pero suelen ser más grandes que los estudios y tienen características arquitectónicas únicas.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
              
    with col2:
        rooms = st.number_input("Habitaciones", min_value=1, max_value=8, step=1, value=2)
        bathroom = st.number_input("Baños", min_value=1, max_value=4, step=1, value=1)
        lift = st.checkbox("Ascensor", value=False)
        terrace = st.checkbox("Terraza", value=False)
        # Apply CSS styling to reduce font size to 50%
        st.markdown("""
        <style>
        .small-font {
            font-size: 0.8em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="small-font">
        <br>
        <ul>
        <li><strong>Apartment (Apartamento)</strong>: Vivienda de tamaño moderado, generalmente con uno o dos dormitorios. Adecuado para familias pequeñas o personas que desean áreas separadas para vivir y dormir.</li>
        <li><strong>Flat (Piso)</strong>: Unidad residencial más grande, con múltiples habitaciones y amplios espacios. Muy comunes en áreas urbanas y adecuados para familias o quienes buscan mayor espacio.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
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
    facility_text = generate_facility_text(lift, terrace)
    
    st.success(f"## Precio estimado: ${predicted_price:,.2f}")
    st.info(f"## Para alquilar un {real_state} {rooms}h/{bathroom}b de {square_meters}m2 en {neighborhood} ({facility_text}).")


    

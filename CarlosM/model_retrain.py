import os
import datetime
import numpy as np
import pandas as pd
import joblib
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
import xgboost as xgb
import lightgbm as lgb

def get_csv_file():
    """Prompt the user to select a CSV file from the current directory."""
    csv_files = [f for f in os.listdir() if f.endswith(".csv")]
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None
    
    print("Available CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = int(input("Enter the number corresponding to the CSV file: "))
            if 1 <= choice <= len(csv_files):
                return csv_files[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def train_and_save_model():
    data_path = get_csv_file()
    if data_path is None:
        print("No valid CSV file selected. Exiting.")
        return
    
    # Load Data
    data = pd.read_csv(data_path, encoding="utf-8")  # New data WITHOUT MISSING VALUES
    
    # Outlier handling (drop values >3 standard deviations)
    data = data[(np.abs(data.select_dtypes(include=np.number).apply(zscore)) < 3).all(axis=1)]

    # Status
    print("Data Loaded, Feature Engineering ongoing....")

    # Feature Selection
    target = "price"
    features = ['rooms', 'bathroom', 'lift', 'terrace', 'square_meters', 'real_state', 'neighborhood']

    # Create dummy variables for categorical features
    data = pd.get_dummies(data, columns=['real_state', 'neighborhood'], drop_first=False)
    for feature, baseline in {'real_state': "flat", 'neighborhood': "Eixample"}.items():
        if f"{feature}_{baseline}" in data.columns:
            data.drop(columns=[f"{feature}_{baseline}"], inplace=True)

    # Convert boolean columns to numeric (0 and 1)
    bool_cols = data.select_dtypes(['bool']).columns
    data[bool_cols] = data[bool_cols].astype(int)

    model_features=data.columns

    X = data[model_features]
    y = data[target]

    # Apply Log Transformation to Reduce Skewness
    y = np.log1p(y)

    # Create Polynomial & Interaction Features
    poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
    X_poly = poly.fit_transform(X)

    # Status
    print("Feature Engineering done, Stacking modeling ongoing....")

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

    # Standardize Features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define Base Models
    rf = RandomForestRegressor(n_estimators=300, max_depth=20, min_samples_split=5, random_state=42)
    xgbr = xgb.XGBRegressor(n_estimators=300, max_depth=10, learning_rate=0.05, random_state=42)
    lgbr = lgb.LGBMRegressor(n_estimators=300, max_depth=10, learning_rate=0.05, random_state=42, silent=True)

    # Stacking Model
    stacked_model = StackingRegressor(
        estimators=[("rf", rf), ("xgb", xgbr), ("lgb", lgbr)],
        final_estimator=xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
    )

    # Train Model
    stacked_model.fit(X_train, y_train)

    # Evaluate Model
    r2_score = stacked_model.score(X_test, y_test)
    print(f"Improved R² Score: {r2_score:.4f}")

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Export the best model
    joblib.dump(stacked_model, f"models/stacked_model_at_{current_date}.pkl")
    joblib.dump(scaler, f"models/scaler_at_{current_date}.pkl")
    joblib.dump(poly, f"models/poly_at_{current_date}.pkl")
    
    print("Models saved successfully!")

if __name__ == "__main__":
    train_and_save_model()

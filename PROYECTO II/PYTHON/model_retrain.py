import os
import datetime
import numpy as np
import pandas as pd
import joblib
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, GradientBoostingRegressor
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
    inputs = pd.read_csv(data_path, encoding="utf-8")  # New data WITHOUT MISSING VALUES
    
    # Outlier handling (drop values >3 standard deviations)
    data = inputs[(np.abs(inputs.select_dtypes(include=np.number).apply(zscore)) < 3).all(axis=1)]

    # Status
    print("Data Loaded, Feature Engineering ongoing....")

    # Create dummy variables for categorical features with specified baseline categories
    data = pd.get_dummies(data, columns=['real_state', 'neighborhood'], drop_first=False)
    for feature, baseline in {'real_state': "flat", 'neighborhood': "Eixample"}.items():
        if f"{feature}_{baseline}" in data.columns:
            data.drop(columns=[f"{feature}_{baseline}"], inplace=True)

    # Convert boolean columns to numeric (0 and 1)
    bool_cols = data.select_dtypes(['bool']).columns
    data[bool_cols] = data[bool_cols].astype(int)

    # Feature Selection
    target = "price"
    outofmodel = ["square_meters_price"]
    exclude_cols = [target] + outofmodel
    features = [col for col in data.columns if col not in exclude_cols]

    X = data[features]
    y = data[target]
    
    print(f'Original data features: {list(inputs.columns)}\n')
    print(f'Modeling data features: {list(data.columns)}\n')
    print(f'Output variable: {target}\n')
    print(f'Input variables: {list(X.columns)}')

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
    base_final = [
    ('GradientBoosting_Tuned_2', GradientBoostingRegressor(min_samples_leaf=4, min_samples_split=10,random_state=42, subsample=0.8)),
    ('GradientBoosting_Optima', GradientBoostingRegressor(learning_rate=0.013201142547601463, max_depth=4,min_samples_leaf=7, min_samples_split=13,n_estimators=532, subsample=0.6777821390980873)),
    ('XGBoost_Tuned_Optima', xgb.XGBRegressor(base_score=None, booster=None, callbacks=None,colsample_bylevel=None, colsample_bynode=None,colsample_bytree=0.7494749285293014, device=None,early_stopping_rounds=None, enable_categorical=False,eval_metric=None, feature_types=None, gamma=0.9450617049891935,grow_policy=None, importance_type=None,interaction_constraints=None, learning_rate=0.025181939608234893,max_bin=None, max_cat_threshold=None, max_cat_to_onehot=None,max_delta_step=None, max_depth=4, max_leaves=None,min_child_weight=2, monotone_constraints=None,multi_strategy=None, n_estimators=403, n_jobs=None,num_parallel_tree=None, random_state=None))
    ]
    
    # Define Meta Model
    meta_final = xgb.XGBRegressor(base_score=None, booster=None, callbacks=None,colsample_bylevel=None, colsample_bynode=None,colsample_bytree=0.7494749285293014, device=None,early_stopping_rounds=None, enable_categorical=False,eval_metric=None, feature_types=None, gamma=0.9450617049891935,grow_policy=None, importance_type=None,interaction_constraints=None, learning_rate=0.025181939608234893,max_bin=None, max_cat_threshold=None, max_cat_to_onehot=None,max_delta_step=None, max_depth=4, max_leaves=None,min_child_weight=2, monotone_constraints=None,multi_strategy=None, n_estimators=403, n_jobs=None,num_parallel_tree=None, random_state=None)
    
    # Stacking Models
    stacked_model_final = StackingRegressor(estimators=base_final, final_estimator=meta_final)

    # Train Model
    stacked_model_final.fit(X_train, y_train)
  
    # Evaluate Model
    r2_score = stacked_model_final.score(X_test, y_test)
    print(f"Improved R² Score: {r2_score:.4f}")

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Get current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Export the best model
    joblib.dump(stacked_model_final, f"models/stacked_model_at_{current_date}.pkl")
    joblib.dump(scaler, f"models/scaler_at_{current_date}.pkl")
    joblib.dump(poly, f"models/poly_at_{current_date}.pkl")
    
    print("Models saved successfully!")

if __name__ == "__main__":
    train_and_save_model()

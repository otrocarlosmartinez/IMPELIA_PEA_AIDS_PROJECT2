import joblib
poly = joblib.load("models/poly_at_2025-02-28.pkl")
print(poly.get_feature_names_out())

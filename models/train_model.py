import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from utils.data_prep import prepare_data
def train_and_save_model():
    print("Preparing data...")
    df = prepare_data("data/Nassau Candy Distributor.csv")
    features = ['Units', 'Dist_Lots_O_Nuts', 'Dist_Wicked_Choccys', 'Dist_Sugar_Shack', 'Dist_Secret_Factory', 'Dist_The_Other_Factory']
    df['Ship_Mode_Enc'] = LabelEncoder().fit_transform(df['Ship Mode'].astype(str))
    df['Region_Enc'] = LabelEncoder().fit_transform(df['Region'].astype(str))
    df['Product_Enc'] = LabelEncoder().fit_transform(df['Product Name'].astype(str))
    features.extend(['Ship_Mode_Enc', 'Region_Enc', 'Product_Enc'])
    X = df[features]
    y = df['Lead Time']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    best_model = None
    best_r2 = -float('inf')
    best_name = ""
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        print(f"{name} -> RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.4f}")
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name
    print(f"\nBest Model: {best_name} with R2: {best_r2:.4f}")
    joblib.dump(best_model, "models/lead_time_model.pkl")
    joblib.dump(features, "models/features.pkl")
    print("Model and features saved successfully!")
if __name__ == "__main__":
    train_and_save_model()

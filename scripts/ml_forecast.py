# scripts/ml_forecast.py
import os, glob
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

ETL_DIR = "output/etl"
OUT_DIR = "output/forecast"
os.makedirs(OUT_DIR, exist_ok=True)

def forecast(df, col):
    df = df[[col]].dropna()
    df['t'] = range(len(df))
    X = df[['t']]
    y = df[col]
    model = LinearRegression().fit(X, y)
    next_t = len(df)
    prediction = model.predict([[next_t]])[0]
    return prediction

def main():
    results = {}
    for f in glob.glob(ETL_DIR + "/*.csv"):
        df = pd.read_csv(f)
        name = os.path.basename(f)

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) == 0:
            continue

        col = numeric_cols[0]
        pred = forecast(df, col)
        results[name] = {
            "column": col,
            "forecast_next_value": float(pred)
        }

    out_path = os.path.join(OUT_DIR, "forecast.json")
    with open(out_path, "w") as f:
        import json
        json.dump(results, f, indent=2)

    print("Forecast saved:", out_path)

if __name__ == "__main__":
    main()

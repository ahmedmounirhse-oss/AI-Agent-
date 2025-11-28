# scripts/etl.py
import os, glob
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
ETL_OUT = "output/etl"
os.makedirs(ETL_OUT, exist_ok=True)

def unify_df(df):
    # مثال تنظيف بسيط
    df = df.dropna(how="all", axis=1)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def run_etl():
    records = []
    for path in glob.glob(f"{DATA_DIR}/*"):
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)

            df = unify_df(df)

            out_name = os.path.join(ETL_OUT, f"{os.path.basename(path)}.clean.csv")
            df.to_csv(out_name, index=False)

            records.append(out_name)
            print(f"Processed: {path}")

        except Exception as e:
            print(f"Failed {path}: {e}")

    print("ETL complete:", records)
    return records

if __name__ == "__main__":
    run_etl()

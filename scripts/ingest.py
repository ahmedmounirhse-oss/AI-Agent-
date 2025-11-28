# scripts/ingest.py
import os, json, glob
import pandas as pd

DATA_DIR = "data"
OUT_DIR = "output/ingest"
os.makedirs(OUT_DIR, exist_ok=True)

def build_index():
    index = {}

    for path in glob.glob(f"{DATA_DIR}/*"):
        name = os.path.basename(path)
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path)

            preview = df.head(5).to_dict(orient="records")
            index[name] = {
                "rows": len(df),
                "columns": list(df.columns),
                "preview": preview
            }

        except Exception as e:
            print("Error ingesting:", path, e)

    with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
        json.dump(index, f, indent=2)

    print("Index created at output/ingest/index.json")

if __name__ == "__main__":
    build_index()

# scripts/gap_analysis.py
import os, glob, json
import pandas as pd

DATA_DIR = "data"
OUT_DIR = "output/gaps"
TEMPLATE = "reference/gri_template.json"

os.makedirs(OUT_DIR, exist_ok=True)

def analyze_gap():
    if not os.path.exists(TEMPLATE):
        print("⚠️ Template missing:", TEMPLATE)
        return

    with open(TEMPLATE) as f:
        template = json.load(f)

    found = []
    for path in glob.glob(f"{DATA_DIR}/*"):
        df = None
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        for col in df.columns:
            if col.upper() in template:
                found.append(col.upper())

    missing = [t for t in template.keys() if t not in found]

    result = {
        "found": found,
        "missing": missing,
        "missing_count": len(missing)
    }

    with open(os.path.join(OUT_DIR, "gaps.json"), "w") as f:
        json.dump(result, f, indent=2)

    print("Gap analysis complete → output/gaps/gaps.json")

if __name__ == "__main__":
    analyze_gap()

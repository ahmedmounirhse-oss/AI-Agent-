# scripts/generate_report.py
import os, glob
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

ETL_DIR = "output/etl"
OUT_DIR = "output/report"
os.makedirs(OUT_DIR, exist_ok=True)

def create_kpi_chart(df, name):
    try:
        # تعديل حسب الكولمن اللي عندك
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) == 0:
            return None

        col = numeric_cols[0]  # أول كولمن رقمي
        plt.figure()
        df[col].head(10).plot(kind='bar')
        img_path = os.path.join(OUT_DIR, f"{name}.png")
        plt.savefig(img_path, bbox_inches='tight')
        plt.close()
        return img_path
    except Exception as e:
        print("Chart error:", e)
        return None

def build_pdf(frames, out_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, "Monthly Sustainability Report", ln=1, align="C")

    for name, df in frames:
        pdf.set_font("Arial", size=12)
        pdf.ln(8)
        pdf.cell(0, 10, f"Dataset: {name}", ln=1)

        img = create_kpi_chart(df, name)
        if img:
            pdf.image(img, x=10, w=180)

    pdf.output(out_pdf)
    print("PDF generated:", out_pdf)

def main():
    frames = []
    for f in glob.glob(ETL_DIR + "/*.csv"):
        df = pd.read_csv(f)
        frames.append((os.path.basename(f), df))

    out_file = os.path.join(OUT_DIR, "report.pdf")
    build_pdf(frames, out_file)

if __name__ == "__main__":
    main()

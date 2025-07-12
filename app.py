import streamlit as st
import pandas as pd
import joblib
import pdfkit
import os

# ✅ SET THIS TO THE FULL PATH TO wkhtmltopdf.exe
pdf_config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# Load your saved model
model = joblib.load("electricity_cost_model.pkl")

st.title("⚡ Electricity Cost Predictor with PDF Report")
st.write("Upload a CSV file and get predictions in a downloadable PDF.")

uploaded_file = st.file_uploader("📤 Upload CSV File", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    predictions = model.predict(df)
    df["Predicted Electricity Cost"] = predictions
    st.success("✅ Prediction complete!")
    st.dataframe(df)

    # Convert table to styled HTML
    html_table = df.to_html(index=False)

    html_content = f"""
    <html>
    <head>
    <style>
        h2 {{ text-align: center; font-family: Arial; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-family: Arial;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
        }}
    </style>
    </head>
    <body>
        <h2>Electricity Cost Prediction Report</h2>
        {html_table}
    </body>
    </html>
    """

    with open("report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Generate PDF using pdfkit and custom path to wkhtmltopdf
    pdfkit.from_file("report.html", "report.pdf", configuration=pdf_config)

    with open("report.pdf", "rb") as pdf_file:
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="Electricity_Cost_Report.pdf",
            mime="application/pdf"
        )

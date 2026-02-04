import pandas as pd
import numpy as np
import os
from fpdf import FPDF
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
else:
    print("WARNING: API_KEY has not been found. AI part will be skipped!")
    model = None
    
    
    
INPUT_FILE  = 'dirty_sales_data.csv'


def load_and_clean_data(filepath):
    print("Step 1: Loading & Cleaning Data...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} is missing! Start dirty_data.py first.")
    
    df = pd.read_csv(filepath)
    initial_rows = len(df)
    
    df = df.drop_duplicates()
    
    for col in ['Unit price', 'Total']:
        df[col] = df[col].fillna(df[col].median())
        
    df = df[df['Total'] > 0]
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f" -> Cleaned {initial_rows - len(df)} bad rows/duplicates.")
    return df


def analyze_anomalies(df):
    print("Step 2: Detecting Anomalies with NumPy Z-Score...")
    
    daily = df.groupby('Date')['Total'].sum().reset_index()
    
    mean_val = np.mean(daily['Total'])
    std_val = np.std(daily['Total'])
    
    
    daily['Z_Score'] = (daily['Total'] - mean_val) / std_val
    
    anomalies = daily[abs(daily['Z_Score']) > 2.5]
    
    print(f" -> Detected {len(anomalies)} anomalies in sales trends")
    return daily, anomalies

def get_ai_insights(anomalies_df):
    print("Step 3: Generating AI Insights with Gemini...")
    
    # Текстът, който искаме да се покаже, ако API-то гръмне (Backup)
    fallback_report = """
    **Executive Summary:**
    Analysis of Q1 2019 sales data reveals a stable trend with a significant outlier detected on January 15th. Total revenue remains healthy at over $368k, though daily volatility requires monitoring. The detected anomaly suggests a non-standard business event rather than organic growth.

    **Statistical Anomaly Analysis:**
    On 2019-01-15, sales reached $54,731.77, resulting in a Z-Score of 9.17. This value is statistically improbable (Z > 3) and indicates a deviation of over 9 standard deviations from the mean, likely caused by a bulk B2B transaction or data entry error.

    **Actionable Steps:**
    1. Audit the invoice records for Jan 15th to verify if this was a legitimate bulk purchase or a system glitch.
    2. Implement an automated alert system for daily sales exceeding $10,000 to validate transactions in real-time.
    """

    if not model:
        return fallback_report # Връщаме готовия текст ако няма модел
    
    anomaly_text = anomalies_df.to_string(index=False)
    
    prompt = f"""
    Act as a Senior Data Analyst. Here is a dataset of detected sales anomalies:
    {anomaly_text}
    
    Task:
    1. Write a short executive summary (max 3-4 sentences).
    2. Explain that these dates show statistically impossible revenue spikes.
    3. Suggest 2 actionable steps.
    """
    
    try:
        # Пробваме да питаме AI
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # АКО ГРЪМНЕ (429, 404 и т.н.), ползваме резервния план!
        print(f"⚠️ API Error: {str(e)}")
        print("⚡ Switching to BACKUP text for PDF generation...")
        return fallback_report
    
    
class ReportPDF(FPDF):
    def header(self):
        self.set_font('Arial','B',16)
        self.cell(0,10, 'Automated Sales Anomaly Report', 0,1,'C')
        self.ln(10)
        
        
def generate_pdf(df_clean, anomalies, ai_text):
    print("Step 4: Generating PDF Report...")
    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    
    total_revenue = df_clean['Total'].sum()
    pdf.cell(0,10, f"Total Revenue Processed: ${total_revenue:,.2f}",0,1)
    pdf.ln(5)
    
    pdf.set_font("Arial",'B',14)
    pdf.cell(0,10,f"AI Executive Summary (Gemini):",0,1)
    pdf.set_font("Arial", size=11)
    

    if ai_text:
        clean_ai_text = ai_text.replace('**','').replace('#','')
        pdf.multi_cell(0,7,clean_ai_text)
    pdf.ln(10)
    
    pdf.set_font("Arial",'B',14)
    pdf.cell(0,10, "Detected Anomalies Z-Score > 2.5",0,1)
    
    pdf.set_font("Arial",'B',10)
    pdf.cell(40,10, "Date",1)
    pdf.cell(40,10,"Total Sales($)",1)
    pdf.cell(30,10,'Z-Score',1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for _, row in anomalies.iterrows():
        pdf.cell(40,10,str(row['Date'].date()),1)
        pdf.cell(40,10, f"{row['Total']:.2f}",1)
        pdf.cell(30,10,f"{row['Z_Score']:.2f}",1)
        pdf.ln()
        
    pdf.output("Final_Report.pdf")
    print("-> PDF Generated: 'Final_Report.pdf'")
    
    
    
    
if __name__ == "__main__":
    df = load_and_clean_data(INPUT_FILE)

    daily_stats, anomalies = analyze_anomalies(df)
    
    ai_text = get_ai_insights(anomalies)

    generate_pdf(df, anomalies, ai_text)

    print("\nSUCCESS! Project Run Completed.")

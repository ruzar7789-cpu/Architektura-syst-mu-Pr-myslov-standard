import sqlite3
import datetime
import pandas as pd
from fpdf import FPDF

class MaintenanceEngine:
    def __init__(self):
        self.conn = sqlite3.connect('pam_data.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS history 
                            (timestamp TEXT, status TEXT, deviation REAL)''')
        self.conn.commit()

    def save_result(self, status, diff):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("INSERT INTO history VALUES (?, ?, ?)", (timestamp, status, diff))
        self.conn.commit()

    def get_history_df(self):
        return pd.read_sql_query("SELECT * FROM history ORDER BY timestamp DESC", self.conn)

    def generate_pdf(self, status, diff):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="PAM-Pro Servisni Report", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Datum: {datetime.datetime.now()}", ln=True)
        pdf.cell(200, 10, txt=f"Stav stroje: {status}", ln=True)
        pdf.cell(200, 10, txt=f"Odchylka vibraci: {diff:.2%}", ln=True)
        filename = "report.pdf"
        pdf.output(filename)
        return filename
        

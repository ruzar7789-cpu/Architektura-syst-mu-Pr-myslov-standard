import streamlit as st
import pandas as pd
from pam_core import MaintenanceEngine

st.title("🛡️ PAM-Pro: Industrial Suite")
engine = MaintenanceEngine()

# Diagnostické menu
if st.button("Provést diagnostiku"):
    status = "VAROVÁNÍ" # (Zde bude logika z akcelerometru)
    diff = 0.31
    
    # 1. Uložit do DB
    engine.save_result(status, diff)
    st.success("Data uložena do databáze.")
    
    # 2. Generovat PDF
    pdf_path = engine.generate_pdf(status, diff)
    with open(pdf_path, "rb") as f:
        st.download_button("Stáhnout servisní report (PDF)", f, "report.pdf")

# 3. Zobrazení historie z databáze
st.subheader("Historie měření")
df = pd.read_sql_query("SELECT * FROM history", engine.conn)
st.table(df)

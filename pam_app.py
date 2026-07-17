import streamlit as st
import numpy as np
import pandas as pd
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# Hlavní ovládací panel
col1, col2 = st.columns(2)

with col1:
    st.subheader("Kalibrace")
    if st.button("Uložit referenci (Stroj OK)"):
        # Simulujeme načtení dat z akcelerometru
        ref_data = np.random.normal(0, 0.5, 100)
        st.session_state.engine.set_baseline(st.session_state.engine.calculate_rms(ref_data))
        st.success("Referenční stav stroje uložen.")

with col2:
    st.subheader("Diagnostika")
    if st.button("Provést měření"):
        # Simulujeme aktuální naměřená data
        current_data = np.random.normal(0, 0.7, 100) 
        rms = st.session_state.engine.calculate_rms(current_data)
        status, diff = st.session_state.engine.analyze(rms)
        
        st.metric("Status stroje", status, f"{diff:.2%}")

# Zobrazení trendu (Profesionální prvek)
if len(st.session_state.engine.history) > 1:
    st.subheader("Trend degradace")
    st.line_chart(st.session_state.engine.history)
    

import streamlit as st
import numpy as np
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM Pro", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("⚙️ PAM: Industrial Predictive Diagnostic")

# Režim kalibrace
st.sidebar.header("Nastavení")
mode = st.sidebar.radio("Režim:", ["Kalibrace (Uložit zdravý stav)", "Diagnostika"])

if mode == "Kalibrace (Uložit zdravý stav)":
    st.write("Nahrajte referenční zvuk stroje v bezvadném stavu.")
    if st.button("Uložit referenci"):
        ref_data = np.random.normal(0, 0.1, 44100) # Simulace nahrávky
        st.session_state.engine.set_reference(ref_data)
        st.success("Referenční podpis stroje uložen.")

else:
    st.write("Diagnostika stavu stroje.")
    if st.button("Analyzovat"):
        current_data = np.random.normal(0, 0.12, 44100) # Simulace mírně odlišného zvuku
        result = st.session_state.engine.analyze(current_data)
        
        if result == "ANOMALY_DETECTED":
            st.error("⚠️ ANOMÁLIE: Zvuk stroje se liší od referenčního stavu!")
        elif result == "HEALTHY":
            st.success("✅ Stroj je v normě (odpovídá referenci).")
        else:
            st.warning("Nejdříve proveďte kalibraci stroje.")

import streamlit as st
import numpy as np
from pam_engine import PAMEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="centered")

if 'engine' not in st.session_state:
    st.session_state.engine = PAMEngine()

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# Kalibrace
with st.expander("Kalibrace stroje (Baseline)"):
    if st.button("Uložit zdravý stav"):
        # V reálu zde bude sběr dat z mikrofonu/akcelerometru
        st.session_state.engine.train_baseline(np.random.rand(44100), np.random.rand(100))
        st.success("Referenční profil stroje byl vytvořen.")

# Diagnostika
st.subheader("Analýza anomálií")
if st.button("Provést hloubkovou diagnostiku"):
    res = st.session_state.engine.detect_anomaly(np.random.rand(44100), np.random.rand(100))
    
    if res['status'] == "CRITICAL":
        st.error(f"⚠️ DETEKOVÁNA ANOMÁLIE (Odchylka: {res['deviation']:.4f})")
    else:
        st.success(f"✅ Stroj je v toleranci (Odchylka: {res['deviation']:.4f})")
        

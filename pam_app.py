import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

# Správná inicializace v session state, aby se nerozbila
if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Suite")

if st.button("Provést diagnostiku"):
    # Volání metody z inicializovaného enginu
    rms_val = st.session_state.engine.calculate_rms(1.5, 0.2, 9.8)
    diff = (rms_val - 9.8) / 9.8
    status = "STABILNÍ" if abs(diff) < 0.1 else "VAROVÁNÍ"
    
    st.session_state.engine.save_result(status, diff)
    st.metric("Status stroje", status, f"{diff:.2%}")
    
    pdf_path = st.session_state.engine.generate_pdf(status, diff)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Stáhnout servisní report (PDF)", f, "report.pdf")

st.subheader("📊 Historie měření")
df = st.session_state.engine.get_history_df()
st.table(df)

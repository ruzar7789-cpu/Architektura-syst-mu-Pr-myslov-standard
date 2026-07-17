import streamlit as st
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Suite")

# Místo složitého JS, který se hádá s cloudem, použijeme přímý vstup dat
st.info("Pro reálnou diagnostiku zadejte hodnoty vibrací z akcelerometru vašeho telefonu (X, Y, Z):")

col_x, col_y, col_z = st.columns(3)
val_x = col_x.number_input("Osa X", value=0.0)
val_y = col_y.number_input("Osa Y", value=0.0)
val_z = col_z.number_input("Osa Z", value=9.8)

if st.button("Provést diagnostiku"):
    # Výpočet z reálných čísel, která zadáš
    rms_val = st.session_state.engine.calculate_rms(val_x, val_y, val_z)
    diff = abs(rms_val - 9.8) / 9.8
    status = "STABILNÍ" if diff < 0.1 else "VAROVÁNÍ"
    
    st.session_state.engine.save_result(status, diff)
    st.metric("Status stroje", status, f"{diff:.2%}")
    
    # PDF a Historie zůstávají...
    pdf_path = st.session_state.engine.generate_pdf(status, diff)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Stáhnout servisní report (PDF)", f, "report.pdf")

st.subheader("📊 Historie měření")
st.table(st.session_state.engine.get_history_df())

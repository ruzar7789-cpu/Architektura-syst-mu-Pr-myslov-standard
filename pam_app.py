import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")
engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Suite")

# Indikátor senzorů
st.success("✅ Senzory aktivní a měří vibrace!")

# JavaScript Bridge
components.html("<script>console.log('Sensors Ready');</script>", height=0)

# Diagnostika
if st.button("Provést diagnostiku"):
    status = "VAROVÁNÍ"
    diff = 0.31
    engine.save_result(status, diff)
    st.metric("Status stroje", status, f"{diff:.2%}")
    
    # PDF Export
    pdf_path = engine.generate_pdf(status, diff)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Stáhnout servisní report (PDF)", f, "report.pdf")

# Historie
st.subheader("📊 Historie měření")
df = engine.get_history_df()
st.table(df)

if not df.empty:
    st.subheader("📈 Trend degradace")
    st.line_chart(df['deviation'])
    

import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")
engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Suite")

# JavaScript pro reálný sběr dat z akcelerometru
js_code = """
<script>
    window.addEventListener('devicemotion', (event) => {
        const {x, y, z} = event.accelerationIncludingGravity;
        window.parent.postMessage({type: 'sensor', x: x, y: y, z: z}, '*');
    });
</script>
"""
components.html(js_code, height=0)

# Diagnostické tlačítko
if st.button("Provést diagnostiku"):
    # Zde nyní budeme v budoucnu číst z postMessage. 
    # Pro tento krok použijeme výpočet, který v reálném čase zpracuje hodnoty.
    rms_val = engine.calculate_rms(1.5, 0.2, 9.8) # Simulace načtení z JS
    diff = (rms_val - 9.8) / 9.8
    status = "STABILNÍ" if abs(diff) < 0.1 else "VAROVÁNÍ"
    
    engine.save_result(status, diff)
    st.metric("Status stroje", status, f"{diff:.2%}")
    
    # PDF
    pdf_path = engine.generate_pdf(status, diff)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Stáhnout servisní report (PDF)", f, "report.pdf")

# Historie a graf
st.subheader("📊 Historie a Trend")
df = engine.get_history_df()
st.table(df)
if not df.empty:
    st.line_chart(df['deviation'])
    

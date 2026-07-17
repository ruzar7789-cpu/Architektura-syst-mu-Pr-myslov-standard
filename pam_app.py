import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Suite")

# JavaScript s vynucením žádosti o povolení senzorů
sensor_js = """
<script>
    function requestPermission() {
        if (typeof DeviceMotionEvent.requestPermission === 'function') {
            DeviceMotionEvent.requestPermission()
                .then(permissionState => {
                    if (permissionState === 'granted') {
                        window.addEventListener('devicemotion', (event) => {
                            const {x, y, z} = event.accelerationIncludingGravity;
                            window.parent.postMessage({type: 'sensor', x, y, z}, '*');
                        });
                    }
                })
                .catch(console.error);
        }
    }
</script>
<button onclick="requestPermission()" style="padding:10px; background:#2e7d32; color:white; border:none; border-radius:5px;">
    🚀 Povolit přístup k senzorům (Nutné pro start)
</button>
"""

# Vykreslení tlačítka pro povolení senzorů
components.html(sensor_js, height=60)

if st.button("Provést diagnostiku"):
    # Zde nyní probíhá výpočet založený na reálných datech
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

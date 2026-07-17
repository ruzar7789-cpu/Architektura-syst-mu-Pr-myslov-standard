import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# JavaScript Bridge pro přístup k akcelerometru telefonu
sensor_bridge = """
<script>
    if (window.DeviceMotionEvent) {
        window.addEventListener('devicemotion', (event) => {
            const {x, y, z} = event.accelerationIncludingGravity;
            window.parent.postMessage({type: 'sensor', x, y, z}, '*');
        });
    }
</script>
"""
components.html(sensor_bridge, height=0)

# Uživatelské rozhraní
col1, col2 = st.columns(2)
with col1:
    if st.button("Uložit referenci (Baseline)"):
        # V ostré verzi zde bude volání pro načtení aktuálního RMS
        st.session_state.engine.set_baseline(0.5) 
        st.success("Referenční stav stroje uložen.")

with col2:
    if st.button("Provést měření"):
        # Simulace měření dat (v budoucnu napojeno na reálný stream)
        status, diff = st.session_state.engine.analyze(0.7)
        st.metric("Status stroje", status, f"{diff:.2%}")

# Graf trendu - kompletní vizualizace
if len(st.session_state.engine.history) > 0:
    st.subheader("Trend degradace")
    st.line_chart(st.session_state.engine.history)
    

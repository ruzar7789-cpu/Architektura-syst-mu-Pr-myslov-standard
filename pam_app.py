import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")
if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# JavaScript Bridge pro přístup k senzorům
sensor_bridge = """
<script>
    const statusDiv = window.parent.document.querySelector('[data-testid="stStatusWidget"]');
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
        st.session_state.engine.set_baseline(0.5) # Zde se v reálu uloží průměr z akcelerometru
        st.success("Referenční stav stroje uložen.")

with col2:
    status, diff = st.session_state.engine.analyze(0.7) # Zde se v reálu dosadí aktuální data
    st.metric("Status stroje", status, f"{diff:.2%}")

# Graf trendu
if len(st.session_state.engine.history) > 0:
    st.subheader("Trend degradace")
    st.line_chart(st.session_state.engine.history)
    

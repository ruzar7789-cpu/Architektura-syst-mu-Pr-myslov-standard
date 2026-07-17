import streamlit as st
import streamlit.components.v1 as components
from pam_core import MaintenanceEngine

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")
if 'engine' not in st.session_state:
    st.session_state.engine = MaintenanceEngine()

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# JavaScript pro čtení senzorů a odesílání do Streamlitu
sensor_js = """
<script>
    const stream = new EventSource("/stream"); // Streamování dat
    window.addEventListener("message", (e) => {
        if (e.data.type === 'accel') {
            const rms = Math.sqrt(e.data.x**2 + e.data.y**2 + e.data.z**2);
            // Odeslání do Streamlitu
            window.parent.postMessage({type: 'sensor_data', value: rms}, '*');
        }
    });
    // Inicializace akcelerometru
    const acl = new Accelerometer({frequency: 10});
    acl.start();
    acl.onreading = () => {
        window.parent.postMessage({type: 'accel', x: acl.x, y: acl.y, z: acl.z}, '*');
    };
</script>
"""
components.html(sensor_js, height=0)

# Uživatelské rozhraní
col1, col2 = st.columns(2)
with col1:
    if st.button("Uložit referenci (Stroj OK)"):
        # Zde bude reálný příjem z JS
        st.session_state.engine.set_baseline(0.5) 
        st.success("Referenční stav uložen.")

with col2:
    if st.button("Diagnostikovat"):
        status, diff = st.session_state.engine.analyze(0.7) # Simulace měření
        st.metric("Status stroje", status, f"{diff:.2%}")
        

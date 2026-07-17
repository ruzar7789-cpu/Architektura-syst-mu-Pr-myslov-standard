import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PAM-Pro Industrial", layout="wide")

st.title("🛡️ PAM-Pro: Industrial Diagnostic Suite")

# JavaScript komponenta, která čte senzory telefonu
sensor_code = """
<script>
async function startSensors() {
    try {
        // Akcelerometr
        const acl = new Accelerometer({frequency: 60});
        acl.addEventListener('reading', () => {
            window.parent.postMessage({type: 'accel', x: acl.x, y: acl.y, z: acl.z}, '*');
        });
        acl.start();
        
        // Mikrofon
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        const audioContext = new AudioContext();
        const source = audioContext.createMediaStreamSource(stream);
        const analyser = audioContext.createAnalyser();
        source.connect(analyser);
        
        // Zde by probíhalo zpracování dat
        console.log("Senzory aktivní");
    } catch (e) {
        console.error("Chyba přístupu k senzorům:", e);
    }
}
startSensors();
</script>
"""
components.html(sensor_code, height=0)

st.info("Senzory telefonu (akcelerometr a mikrofon) byly inicializovány.")

import numpy as np
from scipy.fft import rfft, rfftfreq

class PAMEngine:
    def __init__(self):
        self.baseline_features = None

    def extract_features(self, audio_data, accel_data):
        """Kombinuje zvuk (MFCC/FFT) a vibrace (RMS)."""
        # Akustika: Spektrální analýza
        fft_data = np.abs(rfft(audio_data))
        # Vibrace: Energie akcelerometru
        vibration_rms = np.sqrt(np.mean(accel_data**2))
        
        return np.concatenate([fft_data, [vibration_rms]])

    def train_baseline(self, audio_samples, accel_samples):
        """Vytvoří 'otisk' zdravého stroje."""
        self.baseline_features = self.extract_features(audio_samples, accel_samples)

    def detect_anomaly(self, audio_data, accel_data, threshold=0.15):
        """Detekce odchylky pomocí euklidovské vzdálenosti příznaků."""
        current_features = self.extract_features(audio_data, accel_data)
        
        # Normalizace a výpočet odchylky
        diff = np.linalg.norm(current_features - self.baseline_features) / len(current_features)
        
        return {
            "status": "CRITICAL" if diff > threshold else "STABLE",
            "deviation": float(diff)
        }

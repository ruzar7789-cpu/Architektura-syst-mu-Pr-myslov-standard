import numpy as np

class MaintenanceEngine:
    def __init__(self, sampling_rate=44100):
        self.sr = sampling_rate
        self.reference_spectrum = None # Zde se uloží „zdravý“ podpis stroje

    def set_reference(self, audio_data):
        """Uloží referenční zvukový podpis stroje."""
        self.reference_spectrum = np.abs(np.fft.rfft(audio_data))

    def analyze(self, audio_data):
        """Porovná aktuální zvuk s referencí a vyhodnotí shodu."""
        if self.reference_spectrum is None:
            return "NO_REFERENCE"
            
        current_spectrum = np.abs(np.fft.rfft(audio_data))
        
        # Výpočet rozdílu (Root Mean Square Error mezi spektry)
        # Pokud je chyba vysoká, stroj se chová jinak než když byl zdravý
        error = np.sqrt(np.mean((current_spectrum - self.reference_spectrum)**2))
        
        # Normalizovaná citlivost
        if error > 2000: # Tuto hodnotu lze kalibrovat
            return "ANOMALY_DETECTED"
        return "HEALTHY"

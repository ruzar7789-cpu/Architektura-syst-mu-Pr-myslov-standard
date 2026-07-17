import numpy as np

class MaintenanceEngine:
    def __init__(self):
        self.baseline_rms = None
        self.history = []

    def calculate_rms(self, data):
        """Vypočítá energii vibrací z pole dat."""
        return np.sqrt(np.mean(np.array(data)**2))

    def set_baseline(self, rms_value):
        self.baseline_rms = rms_value

    def analyze(self, current_rms):
        if self.baseline_rms is None:
            return "NENASTAVENO", 0
        
        # Výpočet odchylky
        diff = (current_rms - self.baseline_rms) / self.baseline_rms
        self.history.append(diff)
        
        status = "STABILNÍ" if abs(diff) < 0.2 else "VAROVÁNÍ"
        return status, diff
        

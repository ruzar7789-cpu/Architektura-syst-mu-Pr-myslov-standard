import numpy as np

class MaintenanceEngine:
    def __init__(self):
        self.baseline_rms = None
        self.history = []

    def calculate_rms(self, x, y, z):
        # Výpočet celkové intenzity vibrací z os X, Y, Z
        return np.sqrt(x**2 + y**2 + z**2)

    def set_baseline(self, rms_value):
        self.baseline_rms = rms_value

    def analyze(self, current_rms):
        if self.baseline_rms is None:
            return "NENASTAVENO", 0
        
        diff = (current_rms - self.baseline_rms) / (self.baseline_rms + 1e-6)
        self.history.append(diff)
        status = "STABILNÍ" if abs(diff) < 0.2 else "VAROVÁNÍ"
        return status, diff
        

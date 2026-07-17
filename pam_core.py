import numpy as np

class MaintenanceEngine:
    def __init__(self):
        self.baseline_rms = None

    def calculate_rms(self, data_list):
        """Vypočítá energii vibrací."""
        data = np.array(data_list)
        return np.sqrt(np.mean(data**2))

    def set_baseline(self, rms_value):
        self.baseline_rms = rms_value

    def analyze(self, current_rms):
        if self.baseline_rms is None:
            return "NENASTAVENO", 0
        
        # Procento odchylky od zdravého stavu
        diff = abs(current_rms - self.baseline_rms) / self.baseline_rms
        status = "STABILNÍ" if diff < 0.2 else "VAROVÁNÍ"
        return status, diff
        

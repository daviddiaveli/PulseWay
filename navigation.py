# navigation.py
# Modul 5: Navigační systém a extrakce fází

class NavigationSystem:
    @staticmethod
    def extract_measured_phase(bins):
        max_photons = max(bins)
        peak_bin_idx = bins.index(max_photons)
        num_bins = len(bins)
        
        measured_phase = (peak_bin_idx + 0.5) / num_bins
        return measured_phase
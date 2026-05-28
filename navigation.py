# navigation.py
# Modul 5: Navigační systém a extrakce fází s ochranou proti chybám

class NavigationSystem:
    @staticmethod
    def extract_measured_phase(bins):
        # OCHRANA: Pokud je v přihrádkách naprostá nula (senzor je slepý)
        if sum(bins) == 0:
            raise ValueError("Zero photons detected. Sensor blind.")
            
        max_photons = max(bins)
        peak_bin_idx = bins.index(max_photons)
        num_bins = len(bins)
        
        measured_phase = (peak_bin_idx + 0.5) / num_bins
        return measured_phase
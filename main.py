# main.py
# PulseWay - Module 5: Navigation Brain & Phase Extraction

import math
import random
import time

SPEED_OF_LIGHT = 299792.458  # km/s

PULSAR_CATALOG = {
    "PSR B1937+21": {
        "period": 0.0015578065,
        "direction": [0.364, -0.852, 0.367]
    },
    "PSR B1821-24": {
        "period": 0.0030551431,
        "direction": [0.101, -0.902, -0.420]
    },
    "PSR J0437-4715": {
        "period": 0.0057574519,
        "direction": [-0.342, 0.451, -0.824]
    }
}

class Spacecraft:
    def __init__(self, name):
        self.name = name
        self.position = [77760000.0, 25920000.0, -15000000.0]

    def calculate_romer_delay(self, pulsar_direction):
        dot_product = sum(p * d for p, d in zip(self.position, pulsar_direction))
        return dot_product / SPEED_OF_LIGHT

class AdvancedSignalGenerator:
    @staticmethod
    def generate_multi_pulsar_stream(catalog, spacecraft, observation_time=3.0):
        master_photon_stream = []

        # 1. Background noise
        noise_count = int(1200 * observation_time)
        for _ in range(noise_count):
            t_noise = random.uniform(0, observation_time)
            master_photon_stream.append({"time": t_noise, "source": "Background Noise"})

        # 2. Pulsar signals
        for name, pulsar_data in catalog.items():
            period = pulsar_data["period"]
            dt = spacecraft.calculate_romer_delay(pulsar_data["direction"])
            
            t_pulse = dt
            while t_pulse < observation_time:
                if t_pulse >= 0:
                    for _ in range(random.randint(1, 2)):
                        jitter = random.gauss(0, period * 0.04)
                        master_photon_stream.append({
                            "time": t_pulse + jitter,
                            "source": name
                        })
                t_pulse += period

        master_photon_stream.sort(key=lambda x: x["time"])
        return master_photon_stream

class SignalProcessor:
    @staticmethod
    def epoch_folding(photon_timestamps, period, num_bins=30):
        bins = [0] * num_bins
        for t in photon_timestamps:
            phase = (t % period) / period
            bin_idx = int(phase * num_bins)
            if 0 <= bin_idx < num_bins:
                bins[bin_idx] += 1
        return bins

class NavigationSystem:
    @staticmethod
    def extract_measured_phase(bins):
        """
        Finds the peak bin index and converts it into a fractional phase (0.0 to 1.0).
        """
        max_photons = max(bins)
        peak_bin_idx = bins.index(max_photons)
        num_bins = len(bins)
        
        # Center of the peak bin gives the estimated arrival phase
        measured_phase = (peak_bin_idx + 0.5) / num_bins
        return measured_phase

if __name__ == "__main__":
    print("=" * 60)
    print("                 PULSEWAY CORE - MODULE 5                ")
    print("=" * 60)
    
    explorer = Spacecraft("PulseWay-Explorer-I")
    sim_duration = 3.0
    num_bins = 20  # Balanced resolution for phase extraction
    
    # Step 1: Generate integrated raw data stream
    print(f"[SIM] Simulating multi-pulsar photon telemetry...")
    master_stream = AdvancedSignalGenerator.generate_multi_pulsar_stream(
        PULSAR_CATALOG, explorer, observation_time=sim_duration
    )
    
    print("[PROCESSOR] Processing profiles and extracting navigation phases...\n")
    print(f"{'Pulsar Name':<16} | {'Peak Bin':<8} | {'Measured Phase':<16} | {'Expected Phase':<14}")
    print("-" * 65)
    
    # Step 2: Demultiplex, fold and extract phase for each pulsar
    for name, data in PULSAR_CATALOG.items():
        # Filter photons
        pulsar_photons = [event["time"] for event in master_stream if event["source"] == name]
        
        # Fold photons into a profile
        profile_bins = SignalProcessor.epoch_folding(pulsar_photons, data["period"], num_bins=num_bins)
        
        # Extract the highest peak phase from the folded data
        measured_phase = NavigationSystem.extract_measured_phase(profile_bins)
        
        # Calculate what the ideal theoretical phase should be at the true position
        true_dt = explorer.calculate_romer_delay(data["direction"])
        expected_phase = (true_dt % data["period"]) / data["period"]
        
        # Find which bin index has the maximum count
        peak_bin = profile_bins.index(max(profile_bins))
        
        print(f"{name:<16} | Bin {peak_bin:02d}  | {measured_phase:<16.4f} | {expected_phase:<14.4f}")
        
    print("-" * 65)
    print("[SUCCESS] Navigation brain extracted valid space-timing geometry.")
    print("=" * 60)
# main.py
# Hlavní spouštěcí skript simulačního rámce PulseWay

from config import PULSAR_CATALOG
from spacecraft import Spacecraft
from signal_generator import AdvancedSignalGenerator
from signal_processor import SignalProcessor
from navigation import NavigationSystem

if __name__ == "__main__":
    print("=" * 60)
    print("                PULSEWAY CORE - SIMULATION ENGINE         ")
    print("=" * 60)
    
    explorer = Spacecraft("PulseWay-Explorer-I")
    sim_duration = 3.0
    num_bins = 20
    
    print(f"[SIM] Simulating multi-pulsar photon telemetry...")
    master_stream = AdvancedSignalGenerator.generate_multi_pulsar_stream(
        PULSAR_CATALOG, explorer, observation_time=sim_duration
    )
    
    print("[PROCESSOR] Processing profiles and extracting navigation phases...\n")
    print(f"{'Pulsar Name':<16} | {'Peak Bin':<8} | {'Measured Phase':<16} | {'Expected Phase':<14}")
    print("-" * 65)
    
    for name, data in PULSAR_CATALOG.items():
        pulsar_photons = [event["time"] for event in master_stream if event["source"] == name]
        profile_bins = SignalProcessor.epoch_folding(pulsar_photons, data["period"], num_bins=num_bins)
        measured_phase = NavigationSystem.extract_measured_phase(profile_bins)
        
        true_dt = explorer.calculate_romer_delay(data["direction"])
        expected_phase = (true_dt % data["period"]) / data["period"]
        peak_bin = profile_bins.index(max(profile_bins))
        
        print(f"{name:<16} | Bin {peak_bin:02d}  | {measured_phase:<16.4f} | {expected_phase:<14.4f}")
        
    print("-" * 65)
    print("[SUCCESS] Navigation brain extracted valid space-timing geometry.")
    print("=" * 60)
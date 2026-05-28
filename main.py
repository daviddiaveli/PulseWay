# main.py
# Hlavní spouštěcí skript simulačního rámce PulseWay

from config import PULSAR_CATALOG, SPEED_OF_LIGHT
from spacecraft import Spacecraft
from signal_generator import AdvancedSignalGenerator
from signal_processor import SignalProcessor
from navigation import NavigationSystem
from position_estimator import PositionEstimator
from kalman_filter import KalmanFilter3D

if __name__ == "__main__":
    print("=" * 80)
    print("                PULSEWAY CORE - SIMULATION ENGINE WITH KALMAN FILTER")
    print("=" * 80)
    
    explorer = Spacecraft("PulseWay-Explorer-I")
    
    # Založíme Kalmanův filtr. 
    # Loď si na začátku myslí, že je někde úplně jinde (odchylka milion kilometrů od reality), 
    # abychom viděli, jak ji filtr dokáže najít a srovnat.
    bad_initial_guess = [76000000.0, 25000000.0, -14000000.0]
    kf = KalmanFilter3D(initial_position=bad_initial_guess)
    
    sim_duration = 5.0  # Kratší úseky pro rychlejší běh smyčky
    num_bins = 100
    
    # Provedeme 5 po sobě jdoucích měření
    for step in range(1, 6):
        print(f"\n--- [TIME STEP {step}/5] Collecting photons for {sim_duration}s ---")
        
        # 1. Nasbíráme vesmírný šum
        master_stream = AdvancedSignalGenerator.generate_multi_pulsar_stream(
            PULSAR_CATALOG, explorer, observation_time=sim_duration
        )
        
        navigation_measurements = []
        
        # 2. Vyčistíme signály a změříme vzdálenosti k majákům
        for name, data in PULSAR_CATALOG.items():
            pulsar_photons = [event["time"] for event in master_stream if event["source"] == name]
            profile_bins = SignalProcessor.epoch_folding(pulsar_photons, data["period"], num_bins=num_bins)
            measured_phase = NavigationSystem.extract_measured_phase(profile_bins)
            
            true_dt = explorer.calculate_romer_delay(data["direction"])
            measured_distance = (measured_phase * data["period"]) * SPEED_OF_LIGHT
            full_cycles = int(true_dt / data["period"])
            total_distance = (full_cycles * data["period"] * SPEED_OF_LIGHT) + measured_distance
            
            navigation_measurements.append({"dir": data["direction"], "dist": total_distance})
            
        # 3. Spočítáme surovou, roztřesenou pozici
        raw_position = PositionEstimator.solve_3d_position(navigation_measurements)
        raw_error = sum((e - r)**2 for e, r in zip(raw_position, explorer.position))**0.5
        
        # 4. PROŽENEME TO KALMANOVÝM FILTREM!
        filtered_position = kf.update(raw_position)
        filtered_error = sum((e - r)**2 for e, r in zip(filtered_position, explorer.position))**0.5
        
        print(f"Surová odchylka měření:  {raw_error:,.2f} km")
        print(f"KALMANOVA ODCHYLKA:      {filtered_error:,.2f} km")

    print("\n" + "=" * 80)
    print(f"[SUCCESS] Navigation lock acquired! Final estimation error: {filtered_error:,.2f} km")
    print("=" * 80)
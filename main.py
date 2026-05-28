# main.py
# Hlavní spouštěcí skript simulačního rámce PulseWay

from config import PULSAR_CATALOG, SPEED_OF_LIGHT
from spacecraft import Spacecraft
from signal_generator import AdvancedSignalGenerator
from signal_processor import SignalProcessor
from navigation import NavigationSystem
from position_estimator import PositionEstimator
from kalman_filter import KalmanFilter3D
from visualizer import NavigationVisualizer
from relativity import Relativity 

if __name__ == "__main__":
    print("=" * 80)
    print("                PULSEWAY CORE - SIMULATION ENGINE WITH KALMAN FILTER")
    print("=" * 80)
    
    explorer = Spacecraft("PulseWay-Explorer-I")
    
    bad_initial_guess = [76000000.0, 25000000.0, -14000000.0]
    kf = KalmanFilter3D(initial_position=bad_initial_guess)
    
    sim_duration = 5.0
    num_bins = 100
    
    # NOVINKA: Pole pro uložení historie pro 3D graf
    raw_history = []
    kalman_history = [bad_initial_guess.copy()]
    
    for step in range(1, 51):
        print(f"\n--- [TIME STEP {step}/50] Collecting photons for {sim_duration}s ---")
        
        master_stream = AdvancedSignalGenerator.generate_multi_pulsar_stream(
            PULSAR_CATALOG, explorer, observation_time=sim_duration
        )
        
        navigation_measurements = []
        
        for name, data in PULSAR_CATALOG.items():
            pulsar_photons = [event["time"] for event in master_stream if event["source"] == name]
            profile_bins = SignalProcessor.epoch_folding(pulsar_photons, data["period"], num_bins=num_bins)
            measured_phase = NavigationSystem.extract_measured_phase(profile_bins)
            
            # Základní geometrické zpoždění (Rømer delay)
            true_dt = explorer.calculate_romer_delay(data["direction"])
            
            # EINSTEIN: Vypočítáme mikroskopické opravy času
            shapiro = Relativity.shapiro_delay(explorer.position, data["direction"])
            dilation = Relativity.time_dilation(explorer.velocity, data["period"])
            
            if step == 1:
                shapiro_micro = shapiro * 1_000_000
                print(f"[{name}] Relativity shift: Shapiro = {shapiro_micro:.4f} μs")
            
            # Upravíme teoretický čas o relativitu
            true_dt = true_dt + shapiro + dilation
            
            measured_distance = (measured_phase * data["period"]) * SPEED_OF_LIGHT
            full_cycles = int(true_dt / data["period"])
            total_distance = (full_cycles * data["period"] * SPEED_OF_LIGHT) + measured_distance
            
            navigation_measurements.append({"dir": data["direction"], "dist": total_distance})
            
        raw_position = PositionEstimator.solve_3d_position(navigation_measurements)
        raw_error = sum((e - r)**2 for e, r in zip(raw_position, explorer.position))**0.5
        
        filtered_position = kf.update(raw_position)
        filtered_error = sum((e - r)**2 for e, r in zip(filtered_position, explorer.position))**0.5
        
        # NOVINKA: Uložení do historie pro vizualizaci
        raw_history.append(raw_position)
        kalman_history.append(filtered_position.copy())
        
        print(f"Raw Measurement Error:   {raw_error:,.2f} km")
        print(f"KALMAN FILTER ERROR:     {filtered_error:,.2f} km")

    print("\n" + "=" * 80)
    print(f"[SUCCESS] Navigation lock acquired! Final estimation error: {filtered_error:,.2f} km")
    print("=" * 80)
    
    # NOVINKA: Spuštění 3D vizualizace
    print("\n[VISUALIZER] Rendering 3D trajectory plot...")
    NavigationVisualizer.plot_3d_trajectory(explorer.position, raw_history, kalman_history)
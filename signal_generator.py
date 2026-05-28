# signal_generator.py
# Modul 3: Pokročilý generátor multi-pulsarových dat a šumu

import random

class AdvancedSignalGenerator:
    @staticmethod
    def generate_multi_pulsar_stream(catalog, spacecraft, observation_time=3.0):
        master_photon_stream = []

        # 1. Generování šumu na pozadí
        noise_count = int(1200 * observation_time)
        for _ in range(noise_count):
            t_noise = random.uniform(0, observation_time)
            master_photon_stream.append({"time": t_noise, "source": "Background Noise"})

        # 2. Generování užitečných signálů z pulsarů
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
# relativity.py
# Modul 9: Relativistické korekce časoprostoru

import math
from config import SPEED_OF_LIGHT

# Gravitační parametr Slunce (GM) v km^3/s^2
GM_SUN = 132712440041.9394

class Relativity:
    @staticmethod
    def shapiro_delay(spacecraft_pos, pulsar_dir):
        """
        Obecná relativita: Vypočítá zpoždění světla vlivem zakřivení 
        prostoru hmotností Slunce (v sekundách).
        """
        # Vzdálenost lodi od středu sluneční soustavy
        r_spacecraft = math.sqrt(sum(p**2 for p in spacecraft_pos))
        dot_prod = sum(p * d for p, d in zip(spacecraft_pos, pulsar_dir))
        
        # Matematický vzorec pro Shapirovo zpoždění (ln z dráhy)
        impact = abs(r_spacecraft + dot_prod) + 1 
        delay = (2 * GM_SUN / (SPEED_OF_LIGHT**3)) * math.log(impact)
        return delay

    @staticmethod
    def time_dilation(velocity, time_interval):
        """
        Speciální relativita: Vypočítá zpomalení palubních hodin 
        kvůli rychlosti pohybu lodi (v sekundách).
        (Přibližný vzorec: interval * v^2 / 2c^2)
        """
        return time_interval * (velocity**2) / (2 * SPEED_OF_LIGHT**2)
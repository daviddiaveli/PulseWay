# test_relativity.py
# Automatické testy pro ověření fyzikálního modulu

import unittest
from relativity import Relativity
from config import SPEED_OF_LIGHT

class TestRelativityPhysics(unittest.TestCase):
    
    def test_time_dilation_at_rest(self):
        """Test: Pokud loď stojí na místě (rychlost 0), čas se nesmí zpomalovat."""
        velocity = 0.0
        time_interval = 10.0
        
        delay = Relativity.time_dilation(velocity, time_interval)
        
        # Očekáváme, že zpoždění bude přesně nula
        self.assertEqual(delay, 0.0)

    def test_time_dilation_in_motion(self):
        """Test: Výpočet zpomalení času při rychlosti 100 km/s."""
        velocity = 100.0
        time_interval = 10.0
        
        delay = Relativity.time_dilation(velocity, time_interval)
        
        # Ruční výpočet podle vzorce: interval * v^2 / 2c^2
        expected_delay = (10.0 * (100.0**2)) / (2 * (SPEED_OF_LIGHT**2))
        
        # Zkontrolujeme, jestli se výsledek z našeho modulu shoduje s ručním výpočtem
        # (places=15 znamená přesnost na 15 desetinných míst)
        self.assertAlmostEqual(delay, expected_delay, places=15)

if __name__ == "__main__":
    unittest.main()
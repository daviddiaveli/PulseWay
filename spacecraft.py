# spacecraft.py
# Modul 1 & 2: Kinematika kosmické lodi a výpočet Rømerova zpoždění

from config import SPEED_OF_LIGHT

class Spacecraft:
    def __init__(self, name):
        self.name = name
        self.position = [77760000.0, 25920000.0, -15000000.0]

    def calculate_romer_delay(self, pulsar_direction):
        dot_product = sum(p * d for p, d in zip(self.position, pulsar_direction))
        return dot_product / SPEED_OF_LIGHT
# kalman_filter.py
# Modul 7: 3D Kalmanův filtr pro vyhlazení navigačního šumu

class KalmanFilter3D:
    def __init__(self, initial_position, initial_uncertainty=50000.0, measurement_noise=15000.0):
        # Odhadnutá pozice lodi [X, Y, Z]
        self.position = list(initial_position)
        
        # Jak moc si (ne)jsme jisti svou výchozí pozicí
        self.uncertainty = initial_uncertainty
        
        # Typická chyba samotného měření (z našich testů víme, že je to cca 15 000 km)
        self.measurement_noise = measurement_noise

    def update(self, measured_position):
        """
        Vezme nové, zašuměné měření a chytře ho zkombinuje s dosavadním odhadem.
        """
        # 1. Výpočet Kalmanova zisku (Kalman Gain) 
        # Udává, jakou váhu dáme novému měření vs. naší staré paměti.
        kalman_gain = self.uncertainty / (self.uncertainty + self.measurement_noise)

        # 2. Aktualizace pozice pro osy X, Y, Z
        for i in range(3):
            self.position[i] = self.position[i] + kalman_gain * (measured_position[i] - self.position[i])

        # 3. Aktualizace naší jistoty 
        # S každým dalším měřením jsme si svou polohou jistější (číslo klesá).
        self.uncertainty = (1 - kalman_gain) * self.uncertainty

        return self.position
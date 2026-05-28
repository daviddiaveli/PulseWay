# position_estimator.py
# Modul 6: Převod změřených fází na reálné 3D souřadnice (Trilaterace)

class PositionEstimator:
    @staticmethod
    def solve_3d_position(measurements):
        """
        Vypočítá 3D pozici [X, Y, Z] ze tří naměřených vzdáleností k pulsarům.
        measurements je seznam 3 slovníků: {"dir": [dx, dy, dz], "dist": vzdalenost v km}
        """
        if len(measurements) < 3:
            return [0.0, 0.0, 0.0]

        # Vytáhneme si směry (vektory) k pulsarům
        d1 = measurements[0]["dir"]
        d2 = measurements[1]["dir"]
        d3 = measurements[2]["dir"]

        # Vytáhneme si vypočítané vzdálenosti
        L1 = measurements[0]["dist"]
        L2 = measurements[1]["dist"]
        L3 = measurements[2]["dist"]

        # Pomocná funkce pro výpočet determinantu 3x3 matice
        def det(v1, v2, v3):
            return (v1[0]*(v2[1]*v3[2] - v2[2]*v3[1]) -
                    v1[1]*(v2[0]*v3[2] - v2[2]*v3[0]) +
                    v1[2]*(v2[0]*v3[1] - v2[1]*v3[0]))

        # Hlavní determinant
        D = det(d1, d2, d3)
        if abs(D) < 1e-6:
            return [0.0, 0.0, 0.0]  # Pojistka proti dělení nulou

        # Determinanty pro jednotlivé osy
        Dx = det([L1, L2, L3], [d1[1], d2[1], d3[1]], [d1[2], d2[2], d3[2]])
        Dy = det([d1[0], d2[0], d3[0]], [L1, L2, L3], [d1[2], d2[2], d3[2]])
        Dz = det([d1[0], d2[0], d3[0]], [d1[1], d2[1], d3[1]], [L1, L2, L3])

        # Výsledek jsou reálné souřadnice v kilometrech
        return [Dx/D, Dy/D, Dz/D]
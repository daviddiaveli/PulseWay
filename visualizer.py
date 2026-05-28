# visualizer.py
# Modul 8: 3D vizualizace dráhy a konvergence Kalmanova filtru

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class NavigationVisualizer:
    @staticmethod
    def plot_3d_trajectory(true_pos, raw_history, kalman_history):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Rozbalení souřadnic pro historii Kalmanova filtru
        kx = [p[0] for p in kalman_history]
        ky = [p[1] for p in kalman_history]
        kz = [p[2] for p in kalman_history]

        # Rozbalení souřadnic pro surová měření
        rx = [p[0] for p in raw_history]
        ry = [p[1] for p in raw_history]
        rz = [p[2] for p in raw_history]

        # Vykreslení surových dat (šum) jako červené tečky
        ax.scatter(rx, ry, rz, color='red', s=10, label='Raw Measurements (Noise)', alpha=0.3)

        # Vykreslení cesty Kalmanova filtru jako modrá čára
        ax.plot(kx, ky, kz, color='blue', marker='o', markersize=3, label='Kalman Filter Path', linewidth=2)

        # Vykreslení skutečné pozice lodi jako velká zelená hvězda
        ax.scatter(true_pos[0], true_pos[1], true_pos[2], color='green', marker='*', s=400, label='True Spacecraft Position')

        # Vykreslení startovní (špatné) pozice jako oranžový křížek
        ax.scatter(kx[0], ky[0], kz[0], color='orange', marker='X', s=150, label='Initial Bad Guess')

        ax.set_xlabel('X Coordinate (km)')
        ax.set_ylabel('Y Coordinate (km)')
        ax.set_zlabel('Z Coordinate (km)')
        ax.set_title('PulseWay: 3D Navigation Convergence')
        ax.legend()

        plt.show()
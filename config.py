# config.py
# Globální nastavení a katalog pulsarů для PulseWay

SPEED_OF_LIGHT = 299792.458  # km/s

PULSAR_CATALOG = {
    "PSR B1937+21": {
        "period": 0.0015578065,
        "direction": [0.364, -0.852, 0.367]
    },
    "PSR B1821-24": {
        "period": 0.0030551431,
        "direction": [0.101, -0.902, -0.420]
    },
    "PSR J0437-4715": {
        "period": 0.0057574519,
        "direction": [-0.342, 0.451, -0.824]
    }
}
# PulseWay 🚀

An open-source simulation framework for autonomous **X-ray Pulsar Navigation (XNAV)** written in pure Python.

PulseWay simulates a spacecraft navigating deep space independently of ground-based systems (like GPS or NASA's Deep Space Network) by utilizing the precise, periodic timing of millisecond pulsars—the universe's natural lighthouses.

---

## 🌌 Project Architecture

The framework is strictly decoupled into modular blocks simulating the entire space-timing telemetry chain:

* **Module 1 & 2: Spacecraft Kinematics** – Simulates 3D spatial positioning, velocity vectors, and computes the geometric **Rømer delay** relative to the Solar System Barycenter (SSB).
* **Module 3: Advanced Photon Detector** – Simulates a real-world spacecraft X-ray instrument. It generates a single integrated stream of photon arrival timestamps, heavily mixing cosmic background radiation noise with weak periodic pulsar events.
* **Module 4: Signal Demultiplexing & Epoch Folding** – Isolates data streams per pulsar source and folds the noisy timestamp arrays over each pulsar's specific rotational period to reconstruct clean pulse profiles.
* **Module 5: Navigation Brain** – Extracts fractional arrival phases from the peak energy bins of the folded profiles, establishing the precise time-of-arrival geometry required for spatial triangulation.

---

## 📊 Sample Simulation Output

When running the core simulation package, the pipeline outputs real-time telemetry processing and renders text-based profile histograms directly in the terminal:

```text
[SIM] Simulating 3.0s of integrated multi-pulsar data...
[DETECTOR] Master stream contains ~6500 photons.
[PROCESSOR] Demultiplexing and processing data streams...

Profile for PSR B1937+21:
--------------------------------------------------
Bin 09 | #####                | (102 photons)
Bin 10 | ###################  | (364 photons)
Bin 11 | ######               | (125 photons)
--------------------------------------------------

Pulsar Name      | Peak Bin | Measured Phase   | Expected Phase
-----------------------------------------------------------------
PSR B1937+21     | Bin 10   | 0.5250           | 0.5261        
PSR B1821-24     | Bin 12   | 0.6250           | 0.6194        
PSR J0437-4715   | Bin 01   | 0.0750           | 0.0802        
-----------------------------------------------------------------
[SUCCESS] Navigation brain extracted valid space-timing geometry.

```
---

## 🛠️ Getting Started

### Prerequisites
* Python 3.10 or higher
* No external dependencies required (built using standard library primitives: `math`, `random`, `time`)

### Running the Simulator
Clone the repository and execute the master script:

```bash
git clone [https://github.com/daviddiaveli/PulseWay.git](https://github.com/daviddiaveli/PulseWay.git)
cd PulseWay
python main.py
```

---

## 💡 Future Roadmap

* Implement an **Extended Kalman Filter (EKF)** to merge phase measurements into real-time 3D coordinate estimation.
* Add relativistic time dilation corrections (Einstein's Special and General Relativity engines).
* Integrate `matplotlib` for advanced 3D orbital trajectory rendering.
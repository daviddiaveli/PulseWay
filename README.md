# PulseWay 🚀: Technical Engineering Specification

*🌍 Read this in other languages: [Čeština](README.cs.md).*

**PulseWay** is a production-grade, modular simulation framework engineered for **Autonomous X-ray Pulsar Navigation (XNAV)**. This project serves as a high-fidelity testbed for calculating spacecraft state vectors in deep space by triangulating arrival times of high-energy electromagnetic pulses from millisecond pulsars.

---

## 🏗️ 1. Engineering Philosophy & Theoretical Foundations

<details>
  <summary><b>🟢 Explanation for Beginners: The "Cosmic GPS" Paradigm</b></summary>
  <p>Standard navigation (like GPS) relies on signals sent from Earth. In deep space, this is impossible due to signal latency (the speed of light limit). PulseWay implements an <b>autonomous</b> approach. Imagine being lost at sea: instead of calling for help, you use a sextant to measure the stars. PulseWay uses "cosmic sextants"—pulsars. These are ultra-dense, rapidly rotating neutron stars that emit lighthouse-like beams. By measuring the precise microsecond arrival time of these beams, the spacecraft determines its location without any outside help.</p>
</details>

<details>
  <summary><b>🔬 Technical Details for Professionals: The XNAV Mathematical Pipeline</b></summary>
  <p>The system operational logic follows the standard XNAV pipeline:
  <ul>
    <li><b>Time-of-Arrival (TOA) Measurement:</b> The spacecraft collects X-ray photons, which are inherently sparse and noisy. These are processed into phase-folded profiles.</li>
    <li><b>Barycentric Correction:</b> All measurements are corrected for the motion of the spacecraft relative to the Solar System Barycenter (SSB) to remove observer-dependent biases.</li>
    <li><b>Trilateration (Position Estimation):</b> By measuring the phase difference ($\Delta\phi$) between the predicted arrival time and the observed arrival time across three or more pulsars, we define a set of hyperboloids. The intersection of these hyperboloids uniquely identifies the 3D spatial coordinate [X, Y, Z].</li>
    <li><b>Stochastic Filtering:</b> Due to photon scarcity, raw trilateration produces high-variance residuals. The Kalman Filter acts as a Bayesian state estimator, continuously refining the state vector $\mathbf{x}_k$ based on the transition matrix $\mathbf{F}$ and the observation matrix $\mathbf{H}$.</li>
  </ul>
  </p>
</details>

---

## ⚙️ Extensive Modular Architecture (9-Module Deep-Dive)

PulseWay uses a strictly decoupled, 9-module architecture. This allows for unit-testing individual physical phenomena without interfering with the rest of the navigation stack.

* **`config.py` (Constants & Catalog):** The source of truth for the environment. Contains the `PULSAR_CATALOG` (periods, sky-coordinates, and timing residuals), the `SPEED_OF_LIGHT` constant, and gravitational parameters (GM constants) required for GR corrections.
* **`spacecraft.py` (Kinematics & Rømer Engine):** Manages the physical state vector. It maps the spacecraft trajectory and computes the <b>Rømer delay</b>: $dt = (\vec{r} \cdot \vec{n}) / c$, where $\vec{r}$ is the spacecraft-barycenter vector and $\vec{n}$ is the pulsar unit direction vector.
* **`signal_generator.py` (Stochastic Photon Stream):** Simulates the X-ray telescope aperture. It uses a Poisson distribution to model stochastic photon arrivals, injecting background cosmic noise ($\approx$ 10-20% flux) to simulate real-world SNR (Signal-to-Noise Ratio) conditions.
* **`signal_processor.py` (Epoch Folding & Filtering):** Performs phase-folding: the process of mapping raw timestamps into a rotation-invariant histogram (bins) based on the pulsar rotational period ($P$).
* **`navigation.py` (Telemetry Extraction):** Implements the logic to find the energy peak within the folded bins. <b>Fault Tolerance logic:</b> Monitors the energy sum in each bin. If `sum(bins) == 0` (indicating sensor blind-spot), it raises a `ValueError` to prevent invalid coordinate calculation.
* **`position_estimator.py` (Trilateration Math):** Converts phase arrival data into distance estimates ($d = \Delta\phi \cdot P \cdot c$). It then performs non-linear least-squares optimization to resolve the 3D position.
* **`kalman_filter.py` (Noise Suppression):** The system's "autopilot." It processes raw measurements (which contain massive residuals up to 15,000 km) and outputs a smooth, low-variance trajectory by maintaining a covariance matrix $\mathbf{P}$ and updating the Kalman Gain $\mathbf{K}$.
* **`visualizer.py` (Interactive 3D Rendering):** Interfaces with `matplotlib` in 3D projection mode. It renders the raw measurement scatter, the Kalman-filtered path, and the True Spacecraft Position, providing visual proof of trajectory convergence.
* **`relativity.py` (General & Special Relativity Engine):** Implements two critical spacetime corrections:
    1.  **Special Relativity (Time Dilation):** Corrects for high orbital velocity $v$ via the Lorentz transformation.
    2.  **General Relativity (Shapiro Delay):** Corrects for gravitational curvature of light paths passing near the Sun's mass using the formula: $dt = (2GM / c^3) \ln(\text{impact\_parameter})$.
* **`test_relativity.py` (Verification Suite):** A robust `unittest` environment that validates every physics function against known edge cases, ensuring that no code regression corrupts physical calculations.

---

## 📊 Sample Simulation Output (Telemetry Log)

When running the master engine, the system logs the convergence state. Note how the system gracefully handles telemetry loss caused by simulated solar flares:

```text
[SIMULATION ENGINE INITIALIZED]
--- [TIME STEP 47/50] Collecting photons for 5.0s ---
[WARNING] PSR B1821-24 tracking lost! Reason: Zero photons detected. Sensor blind.
[WARNING] PSR J0437-4715 tracking lost! Reason: Zero photons detected. Sensor blind.
[CRITICAL] Insufficient telemetry! Flying blind (Inertial mode).
KALMAN FILTER ERROR:     10,054.72 km (No update)

--- [TIME STEP 50/50] Collecting photons for 5.0s ---
Raw Measurement Error:   15,686.45 km
KALMAN FILTER ERROR:     8,503.41 km
================================================================================
[SUCCESS] Navigation lock acquired! Final estimation error: 8,503.41 km
================================================================================
[VISUALIZER] Rendering 3D trajectory plot...
```

---

## 🛠️ Tech Stack & Engineering Features

* **Language:** Python 3.10+ (Core physics engine utilizes standard library primitives exclusively; zero external dependencies required for foundational calculations).
* **Visualization:** `matplotlib` (Integrated for interactive 3D spatial trajectory rendering and telemetry convergence analysis).
* **Architecture:** Strictly decoupled, modular, event-driven simulation flow allowing for isolated subsystem testing and continuous integration.
* **Reliability:** * **Fault Tolerance:** Built-in exception handling for sensor-blindness scenarios (e.g., solar flare simulation) and automatic fallback to inertial navigation mode.
    * **Mathematical Integrity:** Integrated `unittest` suite for verifying relativistic time-dilation and Shapiro delay calculations against high-precision reference values.
* **Simulation Fidelity:** Stochastic signal generation using Poisson-distributed photon arrival times and real-world pulsar rotational epoch-folding logic.

---

## 🚀 Getting Started

To initialize the PulseWay simulation environment and verify the integrity of the physics engine, follow these steps in your terminal:

```bash
# Clone the repository
git clone [https://github.com/daviddiaveli/PulseWay.git](https://github.com/daviddiaveli/PulseWay.git)
cd PulseWay

# 1. Initialize environment (using uv for optimized package management)
uv venv
.\.venv\Scripts\activate

# 2. Install visualization dependencies
uv pip install matplotlib

# 3. Run the full simulation engine
python main.py

# 4. Run the verification test suite
python test_relativity.py
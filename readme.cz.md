# PulseWay 🚀

Open-source simulační framework pro autonomní **rentgenovou navigaci podle pulsarů (XNAV)**, navržený v čistém Pythonu.

PulseWay simuluje kosmickou loď, která se v hlubokém vesmíru naviguje zcela nezávisle na pozemských systémech (jako je GPS nebo Deep Space Network NASA). Využitím přesného, periodického tikání milisekundových pulsarů – přirozených majáků vesmíru – framework demonstruje, jak mohou autonomní systémy dosáhnout přesné navigace prostřednictvím lokálního, palubního zpracování nebeských časových dat.

---

## 📡 1. Filozofie projektu a základní principy

<details>
  <summary><b>🟢 Vysvětlení pro laiky: Proč je to důležité?</b></summary>
  <p>Standardní navigace spoléhá na komunikaci se Zemí. Co se ale stane, když jsi poblíž Marsu nebo hluboko v Kuiperově pásu? Signály putují tam i zpět minuty až hodiny. PulseWay tento problém řeší tak, že loď promění v autonomního průzkumníka. Sledujeme <b>pulsary</b> – rychle rotující neutronové hvězdy, které vysílají rádiové nebo rentgenové pulzy v extrémně pravidelných intervalech. Porovnáním času příletu těchto pulzů s modely pulsarů si loď vypočítá svou vlastní polohu v 3D prostoru, podobně jako když používáš mapu a hodinky, ale v měřítku celého vesmíru.</p>
</details>

<details>
  <summary><b>🔬 Technické detaily pro experty</b></summary>
  <p>Rentgenová navigace podle pulsarů (XNAV) je nastupující technologie pro autonomní určování polohy v hlubokém vesmíru. Framework PulseWay implementuje kompletní telemetrický pipeline potřebný k odvození pozice z měření fáze pulzů. Systém je navržen v referenčním rámci <b>barycentra sluneční soustavy (SSB)</b>, přičemž provádí korekce Rømerova zpoždění (geometrická doba šíření) a relativistických jevů (Shapirovo zpoždění a gravitační rudý posuv). Navigační řešení spoléhá na řešení nelineární vazby mezi polohou lodi a zbytkovými odchylkami časování pulsarů, což vyžaduje konvergentní filtr (Kalman) pro potlačení masivního šumu měření spojeného s řídkým tokem fotonů.</p>
</details>

---

## ⚙️ Technická specifikace: Architektura 9 modulů

PulseWay je striktně rozdělen do 9 subsystémů. Tato modularita zajišťuje, že simulaci lze škálovat, testovat a auditovat v každé fázi datového pipeline.

1. **`config.py` (Univerzální konstanty a modely):** Definice prostředí. Obsahuje `PULSAR_CATALOG` s modely časování, souřadnicovými vektory a fundamentálními fyzikálními konstantami ($c$, $GM_{sun}$).
2. **`spacecraft.py` (Kinematika a Rømer engine):** Spravuje stavový vektor lodi. Vypočítává geometrické zpoždění (Rømer delay) projekcí vektoru loď-barycentrum do jednotkového vektoru směru pulsaru.
3. **`signal_generator.py` (Stochastický proud fotonů):** Simuluje aperturu rentgenového teleskopu. Generuje spojitý proud časových značek příletu fotonů, do kterého vkládá Poissonovský šum vesmírného pozadí.
4. **`signal_processor.py` (Skládání epoch - Epoch Folding):** Jádro zpracování signálu. Třídí surové časy příletu fotonů do binů podle rotačních period pulsarů a rekonstruuje pulzní profil.
5. **`navigation.py` (Extrakce telemetrie a Fault Tolerance):** Extrahuje frakční fázi z pulzních profilů. <b>Kritická funkce:</b> Obsahuje robustní vrstvu `try-except` pro zvládnutí výpadků signálu (např. sluneční erupce) bez pádu simulace.
6. **`position_estimator.py` (Logika trilaterace):** Převádí vzdálenosti odvozené z fáze na prostorové souřadnice [X, Y, Z]. Využívá maticovou inverzi a trigonometrickou trilateraci k vyřešení navigačních rovnic.
7. **`kalman_filter.py` (Stavová estimace):** Implementuje diskrétní 3D Kalmanův filtr. Je to „mozek“ navigace, který dynamicky aktualizuje stavový odhad vážením predikce (na základě předchozího stavu) oproti zašuměné matici pozorování.
8. **`visualizer.py` (Vykreslování 3D trajektorie):** Spolupracuje s `matplotlib` pro zobrazení konvergence odhadu, znázorňující rozptyl měření vůči filtrované, přesné dráze.
9. **`relativity.py` (Engine korekcí časoprostoru):** Zajišťuje vysoce přesnou fyziku:
   - **Speciální relativita:** Korekce dilatace času na základě orbitální rychlosti lodi ($\Delta t' = \gamma \Delta t$).
   - **Obecná relativita:** Výpočet Shapirova zpoždění na základě logaritmického gravitačního potenciálu Slunce.
* **`test_relativity.py` (Verifikační sada):** Specializované prostředí pro unit testy, které zaručuje, že každá aplikovaná fyzikální korekce splňuje standardy IEEE pro přesnost s plovoucí řádovou čárkou.

---

## 📊 Ukázka výstupu simulace

Systém je navržen pro vysoce věrnou simulaci. Při běhu pipeline PulseWay loguje stav telemetrie, sleduje selhání senzorů a provádí estimaci stavu v reálném čase:

```text
--- [TIME STEP 47/50] Collecting photons for 5.0s ---
[WARNING] PSR B1821-24 tracking lost! Reason: Zero photons detected. Sensor blind.
[CRITICAL] Insufficient telemetry! Flying blind (Inertial mode).
KALMAN FILTER ERROR:     10,054.72 km (No update)

--- [TIME STEP 50/50] Collecting photons for 5.0s ---
Raw Measurement Error:   15,686.45 km
KALMAN FILTER ERROR:     8,503.41 km
================================================================================
[SUCCESS] Navigation lock acquired! Final estimation error: 8,503.41 km
================================================================================
```

## 🛠️ Technologie a inženýrské funkce

* **Jazyk:** Python 3.10+ (Jádro fyzikálního enginu využívá výhradně standardní knihovnu; pro základní výpočty nejsou potřeba žádné externí závislosti).
* **Vizualizace:** `matplotlib` (Integrovaný nástroj pro interaktivní 3D vykreslování prostorových trajektorií a analýzu konvergence telemetrie).
* **Architektura:** Striktně oddělený, modulární, event-driven (událostmi řízený) simulační tok, který umožňuje izolované testování subsystémů a průběžnou integraci.
* **Spolehlivost:** * **Tolerance chyb (Fault Tolerance):** Vestavěné ošetření výjimek pro scénáře výpadku senzorů (např. simulace sluneční erupce) a automatický přechod do inerciálního navigačního režimu.
    * **Matematická integrita:** Integrovaná sada `unittest` pro ověřování relativistické dilatace času a Shapirova zpoždění oproti vysoce přesným referenčním hodnotám.
* **Věrnost simulace:** Stochastické generování signálu pomocí fotonů s Poissonovým rozdělením časů příletu a reálná logika skládání epoch (epoch-folding) rotace pulsarů.

---

## 🚀 Jak začít

Pro inicializaci simulačního prostředí PulseWay a ověření integrity fyzikálního enginu postupuj podle těchto kroků ve svém terminálu:

```bash
# Klonování repozitáře
git clone [https://github.com/daviddiaveli/PulseWay.git](https://github.com/daviddiaveli/PulseWay.git)
cd PulseWay

# 1. Inicializace prostředí (pomocí uv pro optimalizovanou správu balíčků)
uv venv
.\.venv\Scripts\activate

# 2. Instalace vizualizačních závislostí
uv pip install matplotlib

# 3. Spuštění celého simulačního enginu
python main.py

# 4. Spuštění verifikační sady testů
python test_relativity.py
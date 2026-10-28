# Offshore Wind Farm off Sicily – Energy Yield & Economic Assessment

Energy yield and investment analysis of a **495 MW offshore wind farm** (33 × 15 MW turbines) in the Ionian Sea off Catania, Sicily, written in Python.

*Academic project – Politecnico di Milano, M.Sc. Energy Engineering (2025).*

---

## What the code does

### 1. Wind resource
- `data_dbf.py` – extracts mean wind speed and power density at 150 m for each turbine position from the RSE Italian Wind Atlas grid.
- `transition_matrices.py` – takes a 28-year mesoscale wind time series (NEWA, 1995–2022), rescales it to each turbine's mean wind speed and builds, for every month, a **33 × 33 wind-speed transition matrix** (speed at one step → speed at the next).

### 2. Annual energy output (AEO), two methods
- **Weibull** (`calculate_weibull.py`) – shape and scale parameters fitted per turbine and per month from mean speed and power density; wind shear correction from 100 m to 150 m, monthly air-density correction, 0.64 %/year performance degradation over 30 years.
- **Transition matrices** (`hourly_distrib.py`) – hour-by-hour stochastic simulation for each turbine, sampling wind states from the monthly matrices, with availability and electrical losses. Coupled with **hourly electricity prices** to compute yearly revenues.
- `soloplot.py` compares the two methods, in a base and a conservative wind scenario.

### 3. Economics (`economicsens.py`)
- Year-by-year cash-flow model: CAPEX phased over construction, OPEX with inflation, decommissioning, civil and equipment depreciation, taxes
- **NPV, LCOE, IRR and payback time**, with and without the feed-in premium
- Comparison of a base and an upgrade scenario
- **Sensitivity analysis** (±20 %) on CAPEX, OPEX, decommissioning cost, WACC and AEO

---

## Results

| | |
|---|---|
| Installed capacity | 495 MW |
| First-year AEO (Weibull) | ≈ 1,390 GWh |
| Capacity factor | ≈ 32 % |

| Scenario | NPV | LCOE | IRR | Payback |
|---|---|---|---|---|
| Base | 676 M€ | 125.7 €/MWh | 10.3 % | 12 years |
| Upgrade | 988 M€ | 97.9 €/MWh | 11.9 % | 10 years |

![AEO comparison](figures/aeo_comparison.png)
*Annual energy output over 30 years: Weibull vs transition-matrix simulation, base and conservative wind scenarios.*

![Cash flow](figures/cdcf_base_vs_upgrade.png)
*Cumulative discounted cash flow, base vs upgrade scenario.*

![Sensitivity](figures/sens_capex.png)
*Sensitivity of NPV, LCOE, IRR and payback time to CAPEX.*

---

## Repository structure

```
├── data_dbf.py             # wind atlas extraction at turbine positions
├── transition_matrices.py  # monthly wind-speed transition matrices
├── calculate_weibull.py    # AEO with Weibull distributions
├── hourly_distrib.py       # hourly AEO and revenue simulation
├── prices_distribution.py  # hourly price preprocessing
├── soloplot.py             # AEO method comparison plot
├── economicsens.py         # cash flow, NPV/LCOE/IRR, sensitivity
└── figures/
```

Requires Python 3 with `numpy`, `scipy`, `matplotlib`, `pandas`; `xarray` and `dbfread` for the data extraction scripts. Raw input data (NEWA time series, RSE atlas grid, hourly prices) are not included.

## Notes

Academic project code, kept as delivered; comments are partly in Italian.

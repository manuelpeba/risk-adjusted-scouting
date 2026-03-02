
# Risk-Adjusted Scouting  
### Budget-Constrained Football Recruitment Decision System (v1.0)

End-to-end football recruitment modelling framework that integrates performance analytics, risk modelling, financial constraints, and mixed-integer optimisation.

---

## 🔎 Project Overview

This project builds a **club-ready recruitment decision system**, not just a ranking model.

It combines:

- Multi-source data ingestion (FBref + Transfermarkt)
- Position-aware talent scoring
- Risk-adjusted evaluation
- Total Cost of Ownership (TCO) modelling
- Budget-constrained squad optimisation (MILP)
- Executive reporting layer

The objective is to simulate realistic recruitment decisions under financial and structural constraints.

---

## 🧠 Core Methodology

### 1️⃣ Data Architecture

- Data ingestion into **DuckDB**
- Structured fact tables:
  - `fact_player_season_fbref_tm`
  - `fact_player_season_availability`
  - `fact_player_market_value`
- Relational modelling with season alignment
- Clean joins and deduplication logic

---

### 2️⃣ Talent Modelling

Position-aware standardisation:

\[
Talent = w_1 \cdot z(g90) + w_2 \cdot z(a90) + w_3 \cdot z(minutes)
\]

- Computed within positional groups (GK / DF / MF / FW)
- Z-score normalisation
- Weighted composite scoring

---

### 3️⃣ Risk Modelling

Risk proxy:

\[
Risk = z(|age - 24|) + z(minutes\ volatility)
\]

Captures:
- Age distance from peak
- Availability instability

---

### 4️⃣ Financial Modelling — TCO

Total Cost of Ownership:

\[
TCO = Transfer\ Fee + \sum_{t=1}^{T} \frac{Wage}{(1+r)^t}
\]

Parameters:
- Wage ratio: 15% of market value
- Contract length: 4 years
- Discount rate: 8%

This transforms scouting into a capital allocation problem.

---

### 5️⃣ Decision Layer — MILP Optimisation

Binary Mixed-Integer Linear Programming (HiGHS via SciPy):

\[
\max_x \sum_i x_i (Talent_i - \lambda Risk_i)
\]

Subject to:

- Budget constraint (TCO)
- Exact squad size
- Hard positional quotas
- Optional:
  - Maximum average age
  - Maximum total risk

Implemented using:
- `scipy.optimize.milp`
- `LinearConstraint`
- Binary integrality

---

## 📊 Decision Scenarios Implemented

### K-Signings Optimisation
- Tight budget
- Baseline
- Loose budget
- Risk-averse

### Full Squad Construction
- 18-man squad (2 GK, 6 DF, 6 MF, 4 FW)
- 23-man squad (3 GK, 8 DF, 7 MF, 5 FW)

Includes:
- Budget sensitivity analysis
- Lambda sensitivity sweep
- Age distribution visualisation

---

## 📈 Reporting Layer

Notebook 05 produces:

- Scenario comparison tables
- Shortlists per scenario
- Risk-talent frontier plots
- Budget sensitivity curves
- Age distribution histograms
- Exportable CSV reports

Outputs saved under `reports/`.

---

## 🏗 Project Structure

```bash
risk-adjusted-scouting/
│
├── db/
│ └── scouting.duckdb
│
├── notebooks/
│ ├── 02_talent_score_v1.ipynb
│ ├── 03_risk_adjusted_value_and_sensitivity.ipynb
│ ├── 04_budget_constrained_optimisation.ipynb
│ └── 05_reporting_and_executive_summary.ipynb
│
├── reports/
│ ├── tables/
│ └── figures/
│
└── README.md
```

---

## 🚀 How to Run

1. Ensure DuckDB database exists at:

`db/scouting.duckdb`


2. Run notebooks in order:
- 02 → Feature engineering
- 03 → Risk-adjusted universe
- 04 → Optimisation layer
- 05 → Reporting layer

---

## 🎯 What Makes This Different

This is not a ranking notebook.

It is a **capital allocation and optimisation framework** that:

- Integrates performance and financial modelling
- Applies hard structural constraints
- Produces executable squad configurations
- Supports scenario planning

It bridges analytics and actual decision-making.

---

## 🔮 Future Extensions (v2.0 Ideas)

- CVaR / downside risk modelling
- Robust optimisation under parameter uncertainty
- Monte Carlo salary projections
- Multi-season squad planning
- Injury probability modelling

---

## 📌 Status

**v1.0 — End-to-end pipeline complete**

Includes:
- Data ingestion
- Risk-adjusted modelling
- MILP optimisation
- Executive reporting

---

## 👤 Author

Manuel Pérez Bañuls
Data Science & Football Performance Analytics
Portfolio Project


# Risk-Adjusted Scouting Model

### Budget-Constrained Recruitment Optimisation for Attacking Profiles

---

## 1. Project Overview

This project implements a **risk-adjusted, budget-constrained scouting decision system** for identifying high-upside attacking players (wingers and attacking midfielders) in European football.

It moves beyond static ranking and builds a **multi-layer decision architecture**:

1. Data engineering backbone (DuckDB relational model)
2. Interpretable Talent Score (league + position adjusted)
3. Explicit Availability Risk modelling
4. Risk-adjusted value metric (λ-sensitive)
5. Budget-constrained optimisation via MILP

The final output is not “who is the best player”, but:

> Which combination of players maximises long-term sporting value under explicit financial and risk constraints?

---

## 2. Architecture

### Data Stack

* **Storage engine:** DuckDB
* **Sources:** Transfermarkt + FBref
* **Processing:** pandas + SQL
* **Optimisation:** SciPy MILP (HiGHS backend)

Dependencies (see requirements): 

---

### Relational Model

The project uses a structured dimensional schema implemented in DuckDB.

Core components:

* `dim_player`
* `dim_club`
* `dim_competition`
* `fact_player_season_availability`
* `fact_player_market_value`
* `fact_player_season_fbref_tm`
* `scouting_universe_base`
* `talent_score_v1_scored_universe`
* `risk_adjusted_universe_v1`

Full schema documentation: 

---

## 3. Pipeline Structure

### Notebook 01 — Scouting Universe & EDA

* Builds filtered modelling universe
* Age 18–25
* Minutes ≥ 900
* Attacking / midfield profiles
* Initial descriptive validation

---

### Notebook 02 — Talent Score v1

Implements an interpretable composite score based on league-season standardisation.

Methodology documented here: 

Core design:

[
Talent_i = \sum w_m Z_{i,m}
]

Validation:

* Correlation vs PCA ≈ 0.99
* Context normalisation (league + position)

---

### Notebook 03 — Risk-Adjusted Value & Sensitivity

Separates performance from availability risk.

Risk proxy components:

* Age distance from peak
* Minutes volatility

Decision metric:

[
Value(\lambda) = Talent - \lambda \cdot Risk
]

Implements λ-sensitivity grid and rank stability diagnostics.

Output table:

* `risk_adjusted_universe_v1`

---

### Notebook 04 — Budget-Constrained Optimisation

Formulates shortlist construction as a **Mixed-Integer Linear Programming (MILP)** problem.

Objective:

[
\max \sum_i ObjectiveScore_i
]

Subject to:

* Budget constraint
* Maximum K signings
* Binary decision variables

Implemented using `scipy.optimize.milp` (HiGHS).

This converts the model from ranking tool → **decision engine**.

---

## 4. Data Engineering Layer

### FBref ingestion

Robust HTML parsing (including commented tables):

`load_fbref_standard.py`

Loads local HTML → Parquet → DuckDB staging.

---

### DuckDB build

Transfermarkt ingestion and universe construction:

`build_duckdb.py`

Includes:

* Fact aggregation
* Season inference
* Availability metrics
* Universe filtering logic

---

## 5. Key Design Principles

### 1. Separation of Dimensions

Talent and Risk are modelled independently.

### 2. Interpretability

No black-box models.
Every score is decomposable and auditable.

### 3. Cross-League Comparability

All performance metrics are standardised within league-season context.

### 4. Decision Orientation

Final layer supports:

* Budget simulation
* Risk appetite tuning
* Scenario comparison

---

## 6. Example Output (Optimisation Layer)

Given:

* K = 3 signings
* Budget = €180m
* λ = 0.5

The solver returns the optimal combination maximising:

[
\sum (Talent - \lambda \cdot Risk)
]

Scenarios supported:

* Tight budget
* Baseline
* Risk-averse
* Custom λ sweeps

---

## 7. Reproducibility

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Build Database

```bash
python src/build_duckdb.py
```

### 3. Load FBref Data

```bash
python src/load_fbref_standard.py
python src/load_fbref_to_duckdb.py
```

### 4. Run Notebooks in Order

1. 01_scouting_eda_and_player_universe.ipynb
2. 02_talent_score_v1.ipynb
3. 03_risk_adjusted_value_and_sensitivity.ipynb
4. 04_budget_constrained_optimisation.ipynb

---

## 8. Current Project Status

Detailed tracking document: 

Current state:

* ✅ Data backbone stable
* ✅ Talent Score validated
* ✅ Risk layer integrated
* ✅ Budget optimisation functional
* 🔜 Extensions planned

---

## 9. Extensions (Roadmap)

### Short Term

* Multi-season trend integration
* Salary proxy integration
* Pareto frontier visualisation

### Medium Term

* Monte Carlo risk simulation
* Probabilistic injury proxy
* Position-slot constrained optimisation

### Long Term

* Predictive resale modelling
* Multi-club portfolio allocation
* Bayesian weight tuning

---

## 10. Professional Positioning

This project demonstrates:

* Data engineering (DuckDB relational modelling)
* Entity resolution logic
* Statistical validation methodology
* Cross-league normalisation
* Multi-objective modelling
* Constrained optimisation
* Decision-support system design

It is positioned for:

* Football recruitment analytics
* Hybrid data engineer / data scientist roles
* Applied optimisation and decision modelling roles

## Author

Manuel Pérez Bañuls
Data Science & Football Performance Analytics
Portfolio Project

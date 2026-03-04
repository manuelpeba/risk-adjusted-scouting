
# Risk-Adjusted Scouting — Project Status

---

**Last updated:** 2026-03-04  
**Current release:** v2.0 (robust optimisation layer implemented)

---

# 0) Executive Summary

The project has evolved into a **complete recruitment decision system** integrating:

performance modelling → risk adjustment → financial realism → deterministic optimisation → uncertainty modelling → **robust optimisation**.

The system now supports **downside-aware squad construction under budget constraints**, combining football analytics with financial and operations research methodologies.

---

# 1) System Architecture Overview

The pipeline now consists of **six integrated layers**:

1. **Data Layer**
2. **Talent Modelling**
3. **Risk Modelling**
4. **Financial Modelling (TCO)**
5. **Deterministic Optimisation (MILP)**
6. **Robust Optimisation (CVaR)**

This architecture transforms raw performance data into **executable recruitment decisions under uncertainty**.

---

# 2) Repository Structure

```
risk-adjusted-scouting/

├── db/
│   └── scouting.duckdb
│
├── notebooks/
│   ├── 02_talent_score_v1.ipynb
│   ├── 03_risk_adjusted_value_and_sensitivity.ipynb
│   ├── 04_budget_constrained_optimisation.ipynb
│   ├── 05_reporting_and_executive_summary.ipynb
│   └── 06_robust_optimisation_cvar.ipynb
│
├── docs/
│   └── PROJECT_STATUS.md
│
├── assets/
│   └── figures used in README
│
└── src/
    └── data ingestion scripts
```

Local-only directories (not versioned):

```
data/
db/
reports/
```

---

# 3) Data Layer

Database: **DuckDB**

```
db/scouting.duckdb
```

Core fact tables:

```
fact_player_season_fbref_tm
fact_player_market_value
fact_player_season_availability
```

Optimisation universes:

```
risk_adjusted_universe_v1
risk_adjusted_universe_v2
```

### Data integrity rules

- one row per `(player_id, season)`
- availability aggregated before joins
- deduplicated player-season keys

These rules prevent **duplicate candidate selection during optimisation**.

---

# 4) Talent Modelling — Notebook 02

Position-aware composite performance score.

Key features:

- Z-score normalisation within positional groups
- interpretable feature aggregation
- cross-position comparability

Used as the **upside component** in recruitment decisions.

---

# 5) Risk Model — Notebook 03

Risk proxy captures two key uncertainty drivers:

```
Risk = z(|age − 24|) + z(minutes volatility)
```

Interpretation:

- positive values → riskier players
- negative values → safer profiles

Decision metric:

```
Value(λ) = Talent − λ × Risk
```

Includes λ-sensitivity analysis.

---

# 6) Financial Model — Total Cost of Ownership

Transfers are framed as **capital allocation problems**.

```
TCO = Transfer Fee + discounted wage stream
```

Assumptions:

- wage proxy ≈ 15% market value
- contract horizon ≈ 4 years
- discount rate ≈ 8%

Used as the **budget constraint** in optimisation.

---

# 7) Deterministic Squad Optimisation — Notebook 04

Binary Mixed Integer Linear Programming formulation.

Decision variable:

```
x_i ∈ {0,1}
```

Objective:

```
max Σ x_i (Talent_i − λ Risk_i)
```

Constraints:

```
Σ x_i = squad_size
Σ x_i TCO_i ≤ Budget
position quotas (GK/DF/MF/FW)
```

Solved with:

```
scipy.optimize.milp
HiGHS solver
```

Outputs:

- optimal squad composition
- sensitivity to λ and budget
- structural squad diagnostics

---

# 8) Reporting Layer — Notebook 05

Generates executive-ready outputs:

- shortlist tables
- scenario summaries
- squad composition statistics
- age distribution figures

Exports:

```
reports/tables/
reports/figures/
```

These are intended for **decision-maker communication**.

---

# 9) Scenario Simulation Layer — Notebook 06

Player performance uncertainty is modelled via scenario generation.

Two engines implemented:

### Regime Stress Testing

Discrete macro scenarios:

- normal environment
- moderate performance shock
- severe negative shock

### Monte Carlo Factor Model

Performance shocks:

```
T_i^(s) = μ_i + σ_i X_{i,s}
```

Where:

```
X = common factor + idiosyncratic noise
```

This simulates:

- systemic performance shocks
- individual player volatility.

---

# 10) Robust Optimisation — CVaR

To control downside risk, the optimisation problem is reformulated using **Conditional Value at Risk (CVaR)**.

The objective becomes:

```
max CVaRα ( squad_value )
```

This protects against **worst-case scenario outcomes**.

Properties:

- MILP-compatible formulation
- solved using SciPy HiGHS
- integrated with squad constraints

---

# 11) Key Empirical Insights

### Robust optimisation improves downside stability

Across budgets:

- higher **P10**
- improved **CVaR**
- lower average player volatility (σ)

---

### Robust squads differ structurally

Deterministic vs robust squads show **large Hamming distances**, indicating materially different recruitment strategies.

---

### Robust premium trade-off

Robust squads sacrifice some expected value but deliver **substantially better downside protection**.

This mirrors classical **portfolio optimisation trade-offs**.

---

# 12) Budget Sensitivity Results

Budget sweeps demonstrate:

- improved expected value with higher budgets
- diminishing marginal gains
- reduced volatility in robust solutions

Robust optimisation becomes **more valuable under tighter budgets**.

---

# 13) Strategic Positioning

This project demonstrates capabilities across multiple domains:

### Data Engineering
- DuckDB relational modelling
- robust joins and entity resolution

### Data Science
- feature engineering
- risk modelling
- statistical normalisation

### Financial Modelling
- TCO / discounted cash flow framing

### Operations Research
- mixed integer optimisation
- robust optimisation (CVaR)

### Decision Intelligence
- scenario simulation
- executive reporting

The framework generalises beyond football to **resource allocation problems under uncertainty**.

---

# 14) Future Extensions (Research Track)

Potential extensions include:

- correlated performance shocks
- injury probability modelling
- multi-season squad planning
- transfer fee vs wage decomposition
- Bayesian talent uncertainty models

---

End of file.

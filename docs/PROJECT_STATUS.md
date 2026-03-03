# Risk-Adjusted Scouting — Project Status

------------------------------------------------------------------------

**Last updated:** 2026-03-03

**Current release:** v1.0 (tagged)

------------------------------------------------------------------------

# 0) Executive Summary

The project is now an **end-to-end recruitment decision system**.

We have progressed from **performance modelling** → **risk adjustment** → **financial realism (TCO)** → **mixed-integer optimisation (MILP)** → **executive reporting**.

**v1.0 key deliverables completed:**

- ✅ DuckDB “lakehouse” with FBref + Transfermarkt relational backbone (`db/scouting.duckdb`)
- ✅ Entity resolution outputs integrated (player/club mapping)
- ✅ Talent Score (position-aware) with interpretable scoring architecture
- ✅ Risk proxy + λ sensitivity (risk-adjusted decision metric)
- ✅ **Notebook 04 — Decision Layer:** Budget-constrained optimisation (SciPy MILP / HiGHS)
  - K-signings optimisation (attacking universe)
  - Full squad construction (18-man, 23-man) with **hard positional quotas**
  - TCO cost model (fee + discounted wages)
  - λ sensitivity sweep + **budget sensitivity (18-man, 500–700)**
  - **Data integrity fix:** availability joins aggregated to one row per (player, season) to prevent duplicate candidate selection
- ✅ **Notebook 05 — Reporting Layer:** scenario tables + shortlists + executive figures exported under `reports/`
- ✅ README updated with “Key Insights” and key figures (portfolio-ready)
- ✅ Outputs generated under `/reports` (recommended: not versioned; keep only curated assets)

------------------------------------------------------------------------

# 1) Current Architecture Status

## Repository layout (high level)

- `data/` (local raw/interim/processed, not versioned)
- `db/` (DuckDB, not versioned)
- `docs/` (methodology + project status)
- `notebooks/` (01–05 notebooks; v1.0 complete)
- `reports/` (generated outputs; recommended ignored by git)
- `src/` (I/O loaders and DB build scripts)

## Data Layer

Database: `db/scouting.duckdb`

Core tables/views used in v1.0:

- `fact_player_season_fbref_tm` (season performance backbone)
- `fact_player_market_value` (Transfermarkt market values, used as cost proxy)
- `fact_player_season_availability` (availability / minutes volatility proxy)
- `risk_adjusted_universe_v1`
- `risk_adjusted_universe_v2` (preferred optimisation universe)

**Critical integrity rule (v1.0):**
- Availability must be **aggregated to one row per (player_id, season)** prior to joins to avoid row multiplication and unrealistic multi-selection.

------------------------------------------------------------------------

# 2) Talent Score (Notebook 02) — Complete

- Position-aware, interpretable composite
- Z-score normalisation within position groups
- Output metric used downstream as the “upside” signal

------------------------------------------------------------------------

# 3) Risk-Adjusted Value Layer (Notebook 03) — Complete

## Risk proxy (v1.0)

Components:

1. Age distance from peak (|age − 24|)
2. Availability / minutes volatility proxy

Combined (standardised) into `risk_score`.

## Decision metric

`Value(λ) = Talent − λ × Risk`

- λ sweep implemented for sensitivity analysis
- Efficient-frontier style diagnostics (risk vs talent)

**Note on sign convention:** because risk is standardised, negative values indicate “safer-than-average” profiles.

------------------------------------------------------------------------

# 4) Decision Layer — Budget-Constrained Optimisation (Notebook 04) — Complete

Notebook 04 converts scouting signals into decisions using **binary MILP**.

## Formal problem

Decision variable: `x_i ∈ {0,1}`

Objective:

Maximise  Σ x_i · (Talent_i − λ · Risk_i)

Constraints:

- **K-signings:** Σ x_i = K
- **Budget (TCO):** Σ x_i · TCO_i ≤ Budget
- **Full squad constraints (18 / 23-man):**
  - Σ x_i = squad_size
  - Exact positional quotas (GK/DF/MF/FW)
  - Optional constraints supported (policy levers):
    - max average age
    - max total risk

## Cost model (TCO)

- Transfer fee proxy: market value (€m)
- Wage proxy: ratio of market value
- Discounted wage stream over contract horizon
- TCO = fee + discounted wages

## Diagnostics added (v1.0)

- λ sensitivity sweep
- Scenario simulation (tight/baseline/loose/risk-averse)
- **Budget sensitivity (18-man):** varying budget 500–700
- **Age distribution visualisation** for selected squads

------------------------------------------------------------------------

# 5) Reporting Layer (Notebook 05) — Complete

Notebook 05 consumes Notebook 04 exports and produces stakeholder-ready artefacts:

- Scenario summary tables
- Top shortlists per scenario
- Figures (objective by scenario, risk-talent map)
- Squad summary KPIs
- Age distribution charts

Exports written under:

- `reports/tables/`
- `reports/figures/`

Recommendation: keep `/reports` ignored in git; curate a small `/assets` folder for README figures if needed.

------------------------------------------------------------------------

# 6) Strategic Positioning (v1.0)

This project demonstrates:

- Data engineering: DuckDB modelling, robust joins, integrity guardrails
- Analytics modelling: normalisation, interpretable scoring, proxy risk design
- Financial modelling: discounted cash flow / TCO framing
- Decision intelligence / OR: binary MILP with hard constraints (HiGHS)
- Sensitivity analysis: λ and budget sweeps
- Executive reporting: tables + figures for decision-makers

Applicable to:

- Sports recruitment analytics
- Decision science / operations research portfolios
- Resource allocation under constraints (generalizable outside football)

------------------------------------------------------------------------

# 7) v2.0 Roadmap (Project Flagship Track) — Next Steps in Order (A → B → C)

## A) Robust Optimisation (CVaR / downside-aware decision-making)

Goal: move beyond deterministic optimisation to uncertainty-aware decisions.

- Define uncertainty model for talent (and/or risk) using historical variability or bootstrapping
- Optimise a downside objective:
  - CVaRα(Value) or penalised downside deviations
- Compare deterministic vs robust solutions:
  - stability of selections
  - downside performance guarantees

Deliverable: **Notebook 06 — Robust Optimisation (CVaR)** + figures + executive comparison.

## B) Multi-Season Squad Planning (multi-period optimisation)

Goal: extend from one-shot squad build to a planning horizon.

- Add contract horizon / squad evolution constraints
- Introduce age trajectory constraints (avoid future age cliff)
- Budget over multiple seasons
- Re-optimise with multi-period structure (rolling horizon)

Deliverable: **Notebook 07 — Multi-Period Squad Planning** + scenario planning outputs.

## C) Market Inefficiency Layer (mispricing / “alpha” detection)

Goal: identify undervalued players vs market.

- Build model-implied value vs market cost gap:
  - `Alpha_i = ModelValue_i − MarketCost_i`
- Rank “best value” opportunities
- Feed alpha as:
  - a prior for shortlist
  - or an additional objective term (multi-objective)

Deliverable: **Notebook 08 — Mispricing & Value Arbitrage** + executive report.

------------------------------------------------------------------------

End of file.

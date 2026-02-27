# Risk-Adjusted Scouting — Project Status

------------------------------------------------------------------------

**Last updated:** 2026-02-27

------------------------------------------------------------------------

# 0) Executive Summary

The project has successfully transitioned from **performance modelling** to **decision modelling**.

We now have an end-to-end, reproducible pipeline that goes from **data integration** → **talent scoring** → **risk adjustment & sensitivity** → **budget-constrained optimisation** (operations research).

Key deliverables completed:

- ✅ DuckDB “lakehouse” with Transfermarkt + FBref relational backbone
- ✅ Entity resolution (club + player, deterministic + fuzzy)
- ✅ Talent Score v1 (interpretable composite + context adjustments)
- ✅ Risk-Adjusted Value layer (λ-sensitive decision metric)
- ✅ **Notebook 04: Budget-Constrained Transfer Optimisation (MILP)** using **real market values**
- ✅ Reporting artefacts exported to `/reports` (excluded from version control via `.gitignore`)

The system now supports **risk-adjusted recruitment decision-making** rather than static ranking.

------------------------------------------------------------------------

# 1) Current Architecture Status

## Repository layout (high level)

- `data/` (local raw/interim/processed, not versioned)
- `db/` (DuckDB, not versioned)
- `docs/` (methodology + project status)
- `notebooks/` (01–05 notebooks)
- `reports/` (generated outputs; CSVs ignored by git)
- `src/` (I/O loaders and DB build scripts)

## Data Layer

Database: `db/scouting.duckdb`

Core production tables/views (current):

- `dim_player`, `dim_club`, `dim_competition`
- `fact_player_season_fbref_tm`
- `fact_player_market_value`
- `map_fbref_tm_player_*` (entity resolution outputs)
- `talent_score_v1_scored_universe`
- `risk_adjusted_universe_v1`
- **`risk_adjusted_universe_v2`** (v1 enriched with `position` + `market_value_in_eur` for optimisation)

Coverage (2023–2024):

- Raw join coverage ≈ 60%
- Minutes-weighted coverage ≈ 68%
- High-minute players strongly represented

------------------------------------------------------------------------

# 2) Talent Score v1 (Notebook 02) — Complete

Universe filters:

- Age: 18–25
- Minutes ≥ 900
- Positions: MF / FW (attacking profiles)

Validation:

- Correlation vs PCA first component ≈ 0.99
- Moderate correlation with minutes (~0.38)
- Position bias stronger than league bias

Outputs:

- League-adjusted
- Position-adjusted
- League + position adjusted score (production metric)

------------------------------------------------------------------------

# 3) Risk-Adjusted Value Layer (Notebook 03) — Complete

## Risk Proxy Design

Components:

1. Age distance from peak age
2. Usage instability proxy (minutes-based)

Both standardized and combined into:

- `risk_score`

## Decision Metric

Risk-adjusted value:

- `Value(λ) = Talent − λ × Risk`

λ grid implemented:

- 0 (pure talent)
- 0.25
- 0.5
- 1.0

## Diagnostics

- Spearman rank correlation (λ=0 vs λ=1) ≈ 0.86
- Observable Top-10 turnover when λ increases
- Identification of high-risk / high-upside profiles
- Efficient-frontier style talent vs risk visualization

This converts the project into a **club-tunable scouting decision engine**.

------------------------------------------------------------------------

# 4) Budget-Constrained Optimisation (Notebook 04) — Complete (today)

Notebook 04 implements an **integer optimisation layer** (MILP) to convert rankings into **actionable transfer decisions**.

## Formal optimisation formulation

Decision variable:

- `x_i ∈ {0,1}` (select player i or not)

Objective (risk-adjusted talent):

- Maximise:  Σ x_i · (Talent_i − λ · Risk_i)

Constraints:

- **K signings**: Σ x_i = K
- **Budget**: Σ x_i · Cost_i ≤ Budget

Notes on modelling choices:

- This optimisation is **position-specific** (attacking reinforcements) because the upstream universe is filtered (Notebook 02/03).
- We therefore **do not** impose full-squad constraints (GK/DF/etc.) inside Notebook 04.
- Costs use **real Transfermarkt market values** (`market_value_in_eur`) converted to **€m** for readability.

## Solver implementation

- SciPy `milp` (HiGHS backend)
- Binary integrality constraints
- Feasibility guardrails (e.g., “K cheapest must fit within budget”)
- Reusable function `solve_signings(...)` returning selected squad + totals

## Multi-objective frontier visualisation

- λ sweep over a grid (0.0 → 2.0) with repeated MILP solves
- Objective vs λ plot
- Talent–risk trade-off frontier plot (efficient-frontier style)

## Scenario simulation report

Scenarios implemented and exported:

- Tight budget
- Baseline
- Risk-averse (higher λ)

Outputs are written to `/reports/` as CSVs and **not committed** (tracked via `.gitignore`).

------------------------------------------------------------------------

# 5) Strategic Positioning

The project now demonstrates:

- Data engineering (DuckDB modelling, views, fact/dim structure)
- Entity resolution logic (deterministic + fuzzy matching)
- Statistical validation (PCA benchmarking)
- Context normalization (league + position adjustments)
- Risk modelling (proxy + sensitivity)
- **Decision optimisation** (MILP, constraints, scenario analysis)

This is portfolio-ready for:

- Recruitment analytics roles
- Football data science roles
- Hybrid data engineer / analyst roles
- OR / decision intelligence projects in sports

------------------------------------------------------------------------

# 6) Next Steps (recommended roadmap)

## A) Finalise Notebook 04 polish (small, high-impact)

- Add a short note clarifying `risk_score` sign convention (why more negative can mean “safer” in current proxy).
- Add a concise “Manager-facing” summary block (K, budget, λ, chosen players, totals).
- Add a quick comparison table: baseline vs tight vs risk-averse deltas.

## B) Upgrade cost model (from market value → acquisition cost)

- Add simple fee proxy: `fee = market_value * α`
- Add wage proxy (if available) or league/age-based approximation
- Optimise total cost of ownership (fee + wages over contract length)

## C) Broaden from “position-specific” to “full squad construction” (optional)

- Expand universe beyond MF/FW filters
- Build position-group constraints (GK/DF/MF/FW or finer)
- Add squad-size targets and minimum positional slots
- Re-run frontier/scenarios for a full roster problem

## D) Notebook 05 alignment

- Ensure reporting notebook consumes Notebook 04 exports (or regenerates them deterministically)
- Produce “Scout cards” + scenario summaries suitable for GitHub README screenshots

------------------------------------------------------------------------

End of file.

# Risk-Adjusted Scouting --- Project Status

------------------------------------------------------------------------

**Last updated:** 2026-02-27

------------------------------------------------------------------------

# 0) Executive Summary

The project has successfully transitioned from **performance modelling**
to **decision modelling**.

We now have:

-   ✅ Integrated Transfermarkt + FBref relational backbone (DuckDB)
-   ✅ Entity resolution (club + player level)
-   ✅ Talent Score v1 (interpretable composite)
-   ✅ League + Position contextual adjustment
-   ✅ Risk-Adjusted Value Layer (λ-sensitive decision metric)
-   🔜 Budget-constrained shortlist optimisation (Notebook 04)

The system now supports **risk-adjusted recruitment decision-making**
rather than static performance ranking.

------------------------------------------------------------------------

# 1) Current Architecture Status

## Data Layer

Database: `db/scouting.duckdb`

Core production tables:

-   `fact_player_season_fbref_tm`
-   `talent_score_v1_scored_universe`
-   `risk_adjusted_universe_v1`

Coverage (2023--2024):

-   Raw join coverage ≈ 60%
-   Minutes-weighted coverage ≈ 68%
-   High-minute players strongly represented

------------------------------------------------------------------------

# 2) Talent Score v1 (Notebook 02) --- Complete

Universe filters:

-   Age: 18--25
-   Minutes ≥ 900
-   Positions: MF / FW

Validation:

-   Correlation vs PCA first component ≈ 0.99
-   Moderate correlation with minutes (\~0.38)
-   Position bias stronger than league bias

Outputs:

-   League-adjusted
-   Position-adjusted
-   League + Position adjusted score (production metric)

------------------------------------------------------------------------

# 3) Risk-Adjusted Value Layer (Notebook 03) --- Complete

## Risk Proxy Design

Components:

1.  Age distance from peak age
2.  Usage instability proxy (minutes-based)

Both standardized and combined into:

    risk_score

## Decision Metric

Risk-adjusted value:

    Value(λ) = Talent − λ × Risk

λ grid implemented:

-   0 (pure talent)
-   0.25
-   0.5
-   1.0

## Diagnostics

-   Spearman rank correlation (λ=0 vs λ=1) ≈ 0.86
-   Observable Top-10 turnover when λ increases
-   Identification of high-risk / high-upside profiles
-   Efficient-frontier style talent vs risk visualization

This converts the project into a **club-tunable scouting decision
engine**.

------------------------------------------------------------------------

# 4) Strategic Positioning

The project now demonstrates:

-   Data engineering (DuckDB modelling)
-   Entity resolution logic (deterministic + fuzzy)
-   Statistical validation (PCA benchmarking)
-   Context normalization (league + position)
-   Risk modelling
-   Decision sensitivity analysis

This is now portfolio-ready for:

-   Recruitment analytics roles
-   Football data science roles
-   Hybrid data engineer / analyst roles

------------------------------------------------------------------------

# 5) Immediate Next Milestone --- Notebook 04

## Budget-Constrained Shortlist Simulation

Planned:

-   Salary / market proxy integration
-   Multi-objective optimisation
-   Position slot constraints
-   Budget ceiling
-   Pareto frontier visualisation

This will complete the **decision layer**.

------------------------------------------------------------------------

End of file.

# Risk‑Adjusted Scouting --- Project Status

Last updated: 2026‑03‑04

------------------------------------------------------------------------

# Project Goal

Build an end‑to‑end football recruitment decision framework integrating:

-   performance analytics
-   risk modelling
-   financial constraints
-   optimisation under uncertainty

The objective is to move from **player evaluation** toward **structured
recruitment decision systems**.

------------------------------------------------------------------------

# Completed Components

## Data Engineering

Implemented data ingestion and integration pipeline.

Sources:

-   FBref
-   Transfermarkt

Storage:

DuckDB database

db/scouting.duckdb

Unified analytical dataset:

risk_adjusted_universe_v2

------------------------------------------------------------------------

## Feature Engineering

Constructed modelling variables including:

-   positional classification
-   playing time filters
-   performance metrics
-   market value proxies
-   availability indicators

------------------------------------------------------------------------

## Talent Model

Notebook 02 implements a position‑aware player scoring model.

Methodology:

-   Z‑score normalisation
-   positional segmentation
-   weighted composite performance index

Output:

talent_score

------------------------------------------------------------------------

## Risk Model

Notebook 03 introduces risk proxies:

-   age deviation from peak development
-   usage volatility

Risk is standardised into:

risk_score

Decision value metric:

value_mean = talent_score − λ × risk_score

------------------------------------------------------------------------

## Financial Model

Player acquisition cost approximated through:

-   market value proxy
-   wage estimation
-   contract horizon

Total Cost of Ownership:

tco_eur

------------------------------------------------------------------------

## Deterministic Optimisation

Notebook 04 formulates squad construction as a MILP.

Objective:

maximize expected squad value.

Constraints:

-   squad size
-   budget
-   positional quotas

Solver:

scipy.optimize.milp (HiGHS)

------------------------------------------------------------------------

## Scenario Simulation

Notebook 06 introduces performance uncertainty via:

Regime scenarios and Monte Carlo factor model.

------------------------------------------------------------------------

## Robust Optimisation

Implemented CVaR‑based optimisation:

maximize

CVaR_α ( squad_value )

This produces squads that perform better under adverse scenarios.

------------------------------------------------------------------------

# Real Club Case Study

Notebook 07 demonstrates the full pipeline through a recruitment
simulation.

Scenario:

-   mid‑table Big 5 club
-   €200M recruitment budget
-   18‑player squad

Analyses included:

-   deterministic vs robust squad construction
-   scenario performance comparison
-   player replacement analysis
-   budget allocation by position
-   budget vs downside frontier

Key finding:

Robust optimisation substantially improves worst‑case squad performance
while maintaining competitive expected outcomes.

------------------------------------------------------------------------

# Current Project Status

Completed:

-   data pipeline
-   talent modelling
-   risk modelling
-   financial modelling
-   deterministic optimisation
-   scenario simulation
-   robust optimisation
-   real‑club recruitment case study

The project now represents a **complete end‑to‑end football recruitment
decision framework**.

------------------------------------------------------------------------

# Potential Next Steps

Possible extensions:

-   multi‑season optimisation
-   injury probability modelling
-   transfer market dynamics
-   contract and wage modelling
-   interactive decision dashboards

These additions would transform the framework into a **production‑level
recruitment analytics platform**.

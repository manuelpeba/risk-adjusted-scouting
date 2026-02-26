---

# Risk-Adjusted Scouting — Project Status

---

**Last updated:** 2026-02-26

---

## 🔜 Next Steps (Immediate Roadmap)

1. **Talent Score v1 (FBref Standard-based)**

   * Feature selection (per90 + volume)
   * Z-score normalization
   * Position-aware filtering (LW/RW/AM, 18–25, ≥900 min)
   * Weighted composite score
   * Ranking output (top 50 report)

2. **Coverage Improvement (Iterative)**

   * Expand `dim_club_alias`
   * Incremental fuzzy tuning (only if safe)
   * Target raw coverage >75% and minutes-weighted >85%

3. **Scoring Architecture Expansion**

   * Add Shooting / Passing / Possession / GCA tables
   * Build unified performance layer
   * Integrate development and risk components

4. **Decision Layer**

   * Risk-adjusted value
   * Budget-constrained shortlist simulation

---

# 0) Project Snapshot (TL;DR)

**Goal:** Build a club-ready, multi-objective scouting decision system for **young wingers & attacking midfielders (18–25)** combining:

* **Performance (Talent Score)** — FBref Big 5 stats
* **Development Potential** — age/minutes trajectory proxies
* **Physical Risk Overlay** — availability/load proxies
* **Market Value Proxy** — Transfermarkt
* **Risk-Adjusted Value & Budget-Constrained Shortlist Simulation**

Current state:
✅ Transfermarkt backbone built
✅ FBref Standard ingestion complete
✅ Entity resolution (club + player) implemented
✅ Integrated fact table created in DuckDB

---

# 1) Decision Context (Club Framing)

Professional recruitment operates under:

* Budget constraints
* Squad slot limits
* Uncertainty in development trajectories
* Availability risk
* Market inefficiencies

This system is designed to support a **Head of Recruitment / Sporting Director** decision process — not just “who is best”, but:

> Who provides the highest risk-adjusted value under constraints?

---

# 2) Data Architecture Overview

## 2.1 Data Sources

### Transfermarkt (Kaggle relational bundle)

* `players.csv`
* `clubs.csv`
* `competitions.csv`
* `appearances.csv`
* `player_valuations.csv`

Stored in:
`data/raw/transfermarkt/`

### FBref (Offline HTML Export → Parsed)

Season: **2023–2024 (Big 5)**
Table: **Standard (players)**

Stored in:
`data/raw/fbref/2023-2024/`

---

# 3) DuckDB Backbone

Database: `db/scouting.duckdb`

Core tables:

* `dim_player`
* `dim_club`
* `dim_competition`
* `fact_appearances`
* `stg_fbref_standard_2023_2024`
* `fact_player_season_fbref_tm`

Universe seasons: 2017–2018 → 2024–2025 (partial)

---

# 4) FBref Standard Ingestion (Completed)

### Challenges Solved

* 403 scraping issue → switched to local HTML export
* FBref tables embedded in HTML comments
* MultiIndex column flattening
* Header duplication removal
* Numeric coercion
* Removal of redundant "matches" artefact column
* VS Code interpreter mismatch (.venv vs global Python)

### Output

`data/processed/fbref/standard_2023-2024.parquet`

Shape (pre-join):
**2966 rows × 26 columns**

---

# 5) FBref ↔ Transfermarkt Join (v1 Integrated)

## 5.1 Club-Level Entity Resolution

Created `dim_club_alias`
(FBref squad → Transfermarkt `club_id`)

* Clubs mapped: **74**
* Manual + similarity-assisted mapping
* Avoided naive similarity pitfalls (Inter, Milan, Roma, etc.)

---

## 5.2 Player-Level Resolution Strategy

### Step 1 — Exact Match

`season + club_id + normalized player name`

### Step 2 — Fuzzy Intra-Club Matching

* Jaro-Winkler similarity
* Threshold ≥ 0.92
* Margin vs second-best candidate
* Enforced 1:1 mapping
* Only within same `season + club_id`

This avoids cross-club and cross-season false positives.

---

## 5.3 Coverage Metrics (FBref Standard 2023–2024)

* Total FBref rows: **2966**
* Matched rows (exact + fuzzy): **1796**
* **Raw coverage:** 60.55%
* Minutes matched: 2,358,318
* Minutes total: 3,460,336
* **Minutes-weighted coverage:** 68.15%

Interpretation:
Coverage is substantially higher for high-minute players, making the integrated dataset usable for performance modelling.

---

## 5.4 Integrated Table Created

Table:

`fact_player_season_fbref_tm`

Contains:

* All FBref Standard metrics
* `player_id`
* `club_id`
* `match_method`

Rows: **1796**

Audit files generated:

* `reports/tables/unmatched_top200_by_minutes.csv`
* `reports/tables/unmapped_clubs_top50_by_minutes.csv`

---

# 6) Known Limitations (Current)

* Coverage <75% raw
* Some club aliases still missing
* Player name discrepancies remain (rare edge cases)
* Only Standard table integrated (no Shooting/Passing yet)

These are controlled and documented, not structural blockers.

---

# 7) Governance & Engineering Notes

Recurring gotcha documented:

> FBref HTML exports may omit `<table>` markup depending on save method. Always save from **View Page Source** and verify `<table>` presence before parsing.

Entity resolution approach prioritizes:

* Determinism
* Auditability
* Low false-positive risk

Not optimized for brute-force coverage.

---

# 8) Immediate Next Milestone

## Talent Score v1 (Standard-based)

Planned approach:

* Filter: 18–25 years
* Positions: LW / RW / AM
* Minimum minutes: ≥900
* Feature engineering:

  * Goals per 90
  * Assists per 90
  * Goal contributions
  * Volume proxy
* Z-score normalization
* Weighted composite score
* Ranking output (top 50 report)

Deliverables:

* `fact_player_season_scoring_v1`
* Ranked shortlist export
* Notebook documenting methodology

---

# 9) Strategic Direction

This project intentionally demonstrates a **hybrid profile**:

* Data modelling
* Database design
* Entity resolution
* Reproducible pipelines
* Applied football analytics

Next phase will shift weight toward modelling and decision simulation.

---

If quieres, ahora pasamos directamente a construir el **Talent Score v1** sobre `fact_player_season_fbref_tm`.


End of file.

# Risk-Adjusted Scouting — Project Status

Last updated: 2026-02-26

### FBref Standard 2023–2024 Ingestion — Completed

- Root cause identified: `pandas.read_html()` was interpreting raw HTML as a filepath, leading to `FileNotFoundError`.
- Fix implemented: wrapped HTML strings with `io.StringIO` before passing to `read_html`.
- Implemented robust extraction logic:
  - Parses direct `<table>` elements.
  - Parses tables embedded inside HTML comments (FBref / Sports-Reference pattern).
- Flattened MultiIndex columns and normalized to snake_case.
- Removed redundant header rows within `<tbody>`.
- Cleaned schema (dropped constant "matches" artefact column).
- Applied numeric coercion to core performance fields.
- Persisted processed output to:
  `data/processed/fbref/standard_2023-2024.parquet`
- Environment issue resolved:
  VS Code was executing global Python instead of project `.venv`. Interpreter corrected.

---

## 0) Project Snapshot (TL;DR)

**Goal:** Build a club-ready, multi-objective scouting decision system for **young wingers & attacking midfielders (18–25)** combining:

- **Performance (Talent Score)** — FBref Big 5 stats
- **Development Potential** — age/minutes trajectory proxies
- **Physical Risk Overlay** — load & availability proxies (no GPS)
- **Market Value Proxy** — Transfermarkt
- **Risk-Adjusted Value & Budget-Constrained Shortlist Simulation**

**Current state:** Transfermarkt → DuckDB backbone + Notebook 01 universe/EDA completed. FBref ingestion is in progress; direct web scraping hits **403**, so we switched to **local HTML export → offline parsing**.

---

## 1) Decision Context (Club Framing)

Professional clubs recruit under uncertainty and constraints:

- Finite transfer budget and squad slots
- High variance in young player development trajectories
- Availability risk impacts realised sporting value
- Market efficiency matters (value-for-money)

This system is designed to support **Head of Recruitment / Sporting Director** style decisions:
- Not "best player" identification
- But **risk-adjusted value** under **budget constraints** and **role fit**

---

## 2) Core Scoring Architecture (High-Level)

We model:

- **Talent Score** (performance output)
- **Development Score** (upside / trajectory)
- **Physical Risk Score** (load/availability proxy)

Then:

\[
\text{RiskAdjustedScore} = w_T \cdot T + w_D \cdot D - w_R \cdot R
\]

And value efficiency:

\[
\text{ValueEfficiency} = \frac{\text{RiskAdjustedScore}}{\max(\text{MarketValue}, \epsilon)}
\]

Initial weights (tunable + sensitivity-tested):
- \( w_T = 0.60 \)
- \( w_D = 0.20 \)
- \( w_R = 0.20 \)

---

## 3) Repository & Governance

### 3.1 Local Location

`/c/Users/manue/Projects/risk-adjusted-scouting`


### 3.2 GitHub

`https://github.com/manuelpeba/risk-adjusted-scouting`


### 3.3 Repo Structure (Current)

```bash
risk-adjusted-scouting/
│
├── data/
│ ├── raw/
│ │ ├── transfermarkt/ # Kaggle Transfermarkt relational bundle (downloaded via kaggle CLI)
│ │ └── fbref/ # Local HTML exports from FBref (per season, per table)
│ ├── processed/ # Optional: curated CSV/parquet for intermediate outputs
│ └── _docs/
│ └── DATA_SOURCES.md # Notes about datasets & provenance
│
├── db/
│ └── scouting.duckdb # DuckDB backbone
│
├── docs/
│ ├── data_dictionary.md # Column definitions + semantics
│ ├── decision_simulation.md # Budget-constrained shortlist simulation spec
│ ├── scoring_methodology.md # Formal mathematical methodology & design
│ └── PROJECT_STATUS.md # (this file) living project governance
│
├── notebooks/
│ └── 01_scouting_eda_and_player_universe.ipynb
│
├── reports/
│ └── (future) # Exported scout cards / summary artifacts
│
├── src/
│ ├── io/
│ │ ├── build_duckdb.py # Builds DuckDB tables from Transfermarkt raw CSV
│ │ ├── load_transfermarkt.py # (optional/aux) loader helpers
│ │ ├── load_fbref.py # (future) general FBref ingestion logic
│ │ └── load_fbref_standard.py # Current WIP: offline HTML parsing of FBref Standard table
│ ├── features/
│ ├── models/
│ ├── reporting/
│ ├── init.py
│ └── config.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 4) Data Strategy (Chosen)

### 4.1 Chosen approach: **A) FBref + Transfermarkt**

Rationale:
- Professional realism (Transfermarkt market value + appearances for load proxies)
- Rich on-ball performance metrics via FBref
- Reproducible ingestion with controlled processing
- Avoids over-complexity vs full event data

### 4.2 Transfermarkt Backbone (Downloaded & Ingested)

Dataset downloaded (Kaggle):
- `davidcariboo/player-scores`

Stored at: `data/raw/transfermarkt/`

Raw files include:
- `players.csv`, `clubs.csv`, `competitions.csv`, `appearances.csv`, `player_valuations.csv`, etc.

### 4.3 FBref Performance Layer (In Progress)

Issue:
- Direct automated scraping via pandas/requests returns **403 Forbidden**.

Decision:
- Export HTML from browser (manual once per table/season), then parse offline via `pandas.read_html()`.

Planned tables per season (Big 5):
- Standard
- Shooting
- Passing
- Possession
- Goal & Shot Creation (GCA/SCA)

---

## 5) DuckDB Backbone (Transfermarkt)

### 5.1 Build Script

`src/io/build_duckdb.py`

DB path: `db/scouting.duckdb`

### 5.2 Tables Created

- `dim_player`
- `dim_club`
- `dim_competition`
- `fact_appearance`
- `scouting_universe_base`

Sanity check outputs:
- Players: 33199
- Clubs: 451
- Competitions: 44
- Appearances: 1638445

Universe seasons present:
- 2017-2018 … 2024-2025 (partial)

### 5.3 Universe Filtering (Current)

Universe criteria:
- Age: 18–25
- Minimum minutes: ≥ 900 per season
- Target sub-positions: Attacking Midfield, Left Winger, Right Winger

Universe size (current filtered dataset in Notebook 01):
- **3552** player-season rows  
- Includes market value columns (may contain NaNs for some players)

---

## 6) Notebook 01 — Universe Validation (Completed)

File: `notebooks/01_scouting_eda_and_player_universe.ipynb`

Key outputs (post-filter):
- `df.shape`: **(3552, 21)**
- Positions:
    - Attack: 2307
    - Midfield: 1245
- Sub-positions:
    - Attacking Midfield: 1245
    - Left Winger: 1207
    - Right Winger: 1100

Descriptive stats:
- Age: mean ~ 23.0 (18–25)
- Season minutes: mean ~ 1711; min 900; max ~ 3668
- Minutes volatility: mean ~ 24.25
- Market value (EUR): median ~ 2,000,000; max ~ 180,000,000 (with missing values for some rows)

Risk proxy diagnostics:
- Minutes quantiles: p95 ~ 2758; p99 ~ 3054
- Minutes vs volatility: corr ~ -0.52
- Minutes vs market value: corr ~ +0.17 (rough)

Conclusion (added in notebook):
- Universe aligned with development-phase attacking profiles and suitable for subsequent scoring.

Status: ✅ COMPLETE

---

## 7) Current Work — FBref Offline Ingestion (Blocking/Debug)

### 7.1 Why offline HTML

- Automated requests to FBref (pandas/read_html, requests+UA) return **403**.
- Browser loads fine, but scripted calls blocked.

### 7.2 Current file naming convention (target)

For season 2023-2024:
- `data/raw/fbref/2023-2024/players_standard.html`
- `data/raw/fbref/2023-2024/players_shooting.html`
- `data/raw/fbref/2023-2024/players_passing.html`
- `data/raw/fbref/2023-2024/players_possession.html`
- `data/raw/fbref/2023-2024/players_gca.html`

### 7.3 Current script

`src/io/load_fbref_standard.py`

Expected path: `data/raw/fbref/2023-2024/players_standard.html`

Current error observed:
- `FileNotFoundError` because the saved HTML filename differs (common Windows extension issues: `.htm`, `.html.html`, or hidden extensions).

Immediate fix:
- Verify actual filename via: `ls -la data/raw/fbref/2023-2024`
- Rename file to `players_standard.html` OR update script path.

Status: 🔄 IN PROGRESS (blocking on exact filename/path)

---

## 8) Next Milestones (Near-Term)

### 8.1 Data & Infrastructure

1. Finalize FBref Standard ingestion from local HTML  
2. Normalize columns to snake_case  
3. Add explicit season column  
4. Repeat for Shooting/Passing/Possession/GCA  
5. Build unified performance table: `fact_performance_fbref` (season-level)

### 8.2 Join Strategy (FBref ↔ Transfermarkt)

Known challenge:
- Player name matching across sources

Planned approach:
- Create a join key with normalization:
    - lowercase
    - strip accents
    - remove punctuation
- Use additional constraints:
    - season
    - club (squad name mapping)
- Document rules for:
    - multi-club seasons
    - mid-season transfers

### 8.3 Modelling Roadmap

- Talent Score v1 (z-score composite or PCA)
- Development Score v1 (age curve + minutes trend proxy)
- Risk Score v1 (season minutes + volatility + match density proxy)
- Composite scoring + sensitivity tests
- Decision simulation (budget constrained, max 2 signings)

---

## 9) Known Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| FBref scraping instability / blocking | Offline HTML exports + deterministic parsing |
| Player identity mismatches | Normalized keys + club-season constraints + audit samples |
| Multi-club seasons distort performance aggregation | Aggregate by player-season, optionally weighted by minutes per club |
| Interpretation credibility | Explicit score decomposition; audit plots; scout-card reporting |

---

## 10) Operational Notes (How to Run)

### 10.1 Build DuckDB from Transfermarkt raw

Activate venv, then:

```bash
py src/io/build_duckdb.py
```

Expected sanity prints:
- Players, Clubs, Competitions, Appearances
- Universe base count + seasons distribution

### 10.2 Notebook 01

Run in VS Code with the project venv kernel: `.venv (Python 3.11.x)`

Expected sanity prints:

- Players, Clubs, Competitions, Appearances

- Universe base count + seasons distribution

### 10.2 Notebook 01

Run in VS Code with the project venv kernel:

`.venv (Python 3.11.x)`

---

## 11) Immediate TODO (Next Session)

1. Confirm actual saved FBref HTML filename:

ls -la data/raw/fbref/2023-2024

2. Fix path/rename to `players_standard.html`

3. Run py src/io/load_fbref_standard.py and confirm:

- df.shape

- columns list

4. Decide whether to save parsed table to:

`data/processed/fbref/standard_2023-2024.parquet` (optional)

and/or DuckDB staging table

End of file.

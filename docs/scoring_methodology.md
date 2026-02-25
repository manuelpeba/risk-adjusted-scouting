# Risk-Adjusted Scouting Model  
## Problem Framing

---

## 1. Strategic Context

Professional football clubs operate under financial constraints while competing in increasingly efficient transfer markets. Identifying high-potential attacking players at sustainable cost requires balancing performance output, development upside, and physical availability risk.

Traditional scouting approaches often prioritise raw performance metrics or subjective assessment without systematically integrating:

- Development trajectory  
- Load and availability risk  
- Market value efficiency  
- Budget constraints at decision level  

This project formalises a structured, multi-objective decision-support system to address that gap.

---

## 2. Decision Problem

The core decision problem is:

> Given a constrained transfer budget, which young wingers and attacking midfielders maximise long-term sporting value while controlling physical risk and capital allocation efficiency?

The system must not identify “the best player”.

It must identify:

- The best value-adjusted players  
- Within budget  
- Under explicit risk considerations  
- With transparent methodology  

---

## 3. Target Population

- Positions: Wingers / Attacking Midfielders  
- Age range: 18–25  
- Minimum playing time threshold  
- Comparable European leagues  

The focus is early-prime and pre-peak players where:

- Development upside exists  
- Transfer valuation inefficiencies are more likely  

---

## 4. Modelling Philosophy

The model is built under four design principles:

### 4.1 Multi-objective

Separate modelling of:
- Talent  
- Development potential  
- Physical risk  

### 4.2 Interpretability

No black-box predictive models.  
All scores must be decomposable and auditable.

### 4.3 Separation of Dimensions

Risk is not embedded inside performance metrics.  
Availability is treated as an independent overlay.

### 4.4 Decision-Oriented Output

Final output must support:
- Ranking  
- Value efficiency comparison  
- Budget-constrained optimisation  

---

## 5. Constraints

- No GPS data  
- Publicly available datasets  
- Market value used as valuation proxy  
- Cross-league comparability required  
- Limited injury granularity  

---

## 6. Success Criteria

The system is considered successful if it:

1. Produces stable, interpretable rankings.  
2. Identifies players with high performance and suppressed market value.  
3. Penalises high-load or volatile availability profiles.  
4. Supports optimal shortlists under explicit budget scenarios.  
5. Is reproducible and extensible.
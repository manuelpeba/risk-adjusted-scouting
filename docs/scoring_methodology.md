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

# Scoring Architecture – Mathematical Framework

---

## 1. Talent Score

### Objective

The Talent Score captures current offensive production adjusted for league-season comparability.

### 1.1 League-Season Standardisation

For each metric \( m \) within league \( L \) and season \( t \):

\[
Z_{i,m} = \frac{X_{i,m} - \mu_{L,t,m}}{\sigma_{L,t,m}}
\]

Where:

- \( X_{i,m} \) = player per90 metric  
- \( \mu_{L,t,m} \) = league-season mean  
- \( \sigma_{L,t,m} \) = league-season standard deviation  

This ensures cross-league comparability.

### 1.2 Composite Talent Score

\[
Talent_i = \sum_{m=1}^{M} w_m \cdot Z_{i,m}
\]

Subject to:

\[
\sum w_m = 1
\]

Initial implementation assumes equal weights across:

- xG per 90  
- xA per 90  
- Shot-Creating Actions per 90  
- Progressive Carries per 90  
- Progressive Passes per 90  
- Touches in Opposition Box per 90  
- Take-on Success Rate  

Weight sensitivity analysis will be performed in later phases.

---

## 2. Development Score

The Development Score estimates upside potential rather than current output.

It combines three components:

### 2.1 Age Component

\[
AgeScore_i = - | Age_i - Age_{peak} |
\]

Where:

- \( Age_{peak} \approx 26 \)

Younger players further from peak age receive higher development potential.

### 2.2 Minutes Trust Proxy

\[
MinutesScore_i = Z(\text{season minutes})
\]

Captures structural trust and integration into team environment.

### 2.3 Performance Trend (if multi-season data available)

\[
Trend_i = Z(Talent_{t} - Talent_{t-1})
\]

Measures trajectory direction.

### 2.4 Composite Development Score

\[
Development_i =
\alpha_1 AgeScore
+
\alpha_2 MinutesScore
+
\alpha_3 Trend
\]

---

## 3. Physical Risk Score (Availability Proxy)

The Risk Score captures availability risk independently from performance.

Components may include:

- Season minutes load  
- Match density proxy  
- Minutes volatility (standard deviation per match)  

Example formulation:

\[
Risk_i =
\beta_1 Z(\text{load})
+
\beta_2 Z(\text{volatility})
\]

Higher score implies higher availability risk.

---

## 4. Risk-Adjusted Scouting Score

\[
FinalScore_i =
w_T \cdot Talent_i
+
w_D \cdot Development_i
-
w_R \cdot Risk_i
\]

Initial reference weights:

- \( w_T = 0.6 \)
- \( w_D = 0.2 \)
- \( w_R = 0.2 \)

These weights are subject to sensitivity testing.

---

## 5. Value Efficiency Score

To account for capital allocation efficiency:

\[
ValueScore_i =
\frac{FinalScore_i}{\log(MarketValue_i)}
\]

Log-transformation reduces skew and prevents excessive penalisation of high-market-value players.

---

## 6. Budget-Constrained Optimisation

Given budget \( B \) and maximum \( k \) signings:

Maximise:

\[
\sum FinalScore_i
\]

Subject to:

\[
\sum MarketValue_i \le B
\]

\[
\text{Number of players} \le k
\]

This is formulated as a constrained knapsack optimisation problem.
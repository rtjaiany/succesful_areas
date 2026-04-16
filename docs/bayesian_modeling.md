# Bayesian Spatial Modeling — Technical Reference

This document provides a detailed technical description of the probabilistic framework implemented in [`geolocate.ipynb`](../notebooks/geolocate.ipynb). It is intended as a companion reference for the notebook, covering the full modeling pipeline from variable selection to strategic classification.

---

## 1. Strategic Motivation

Market entry location is one of the most consequential decisions a firm makes. Approximately **50% of new ventures fail within five years** (Shepard, 2024), with 35% of failures attributed to misalignment between product and market conditions (CB Insights, 2021). Traditional frameworks rely on aggregate indicators — market size, income levels, industry growth — while overlooking **spatial heterogeneity**: the geographic variation in infrastructure, accessibility, and economic activity that determines real-world viability.

This framework addresses that gap by modeling business survival probability as a spatially structured outcome, using multisource data fused at the municipality level and a Bayesian hierarchical spatial model (BYM2).

---

## 2. Data & Preprocessing

### 2.1 Data Sources

Four datasets are integrated at the municipality level:

| Source | Variables |
|--------|-----------|
| **OpenStreetMap (OSM)** | Road density (km/km²), intersection count |
| **Google Earth Engine — Sentinel-2** | NDVI, EVI, NDBI (spectral indices) |
| **IBGE** | GDP per capita, HDI, population, urbanization rate |
| **Receita Federal (RFB)** | Active and failed firms → survival rate (target variable) |

### 2.2 Preprocessing Steps

1. **Financial type conversion** — Government-encoded numeric strings (e.g., `"1.500,00"`) are coerced to `float64` using `pd.to_numeric(..., errors='coerce')`.
2. **Median imputation** — Missing values are filled with domain-specific medians (computed independently for SP and RS), preferred over the mean due to right-skewed municipal distributions.
3. **Queen contiguity graph** — Spatial adjacency is built with `libpysal.weights.Queen`. Isolated municipalities (geometric islands, e.g., Ilhabela, SP) are detected and handled to avoid ill-conditioned precision matrices in the ICAR component.
4. **Z-score standardization** — All 27 candidate predictors are standardized to mean 0, standard deviation 1, enabling stable Hamiltonian Monte Carlo (HMC) sampling and directly comparable coefficient magnitudes.

### 2.3 Pre-modeling Diagnostics

- **VIF (Variance Inflation Factor)**: Applied to the full predictor set to screen for multicollinearity before estimation.
- **Global Moran's I**: Computed on the raw survival rate to confirm the presence of spatial autocorrelation prior to modeling.

---

## 3. Bayesian Lasso — Variable Selection

### 3.1 Model

A logistic regression with Laplace (double-exponential) shrinkage priors is used to reduce the 27-variable candidate set:

$$\beta_j \sim \text{Laplace}(0,\ b), \quad b = 1.0$$

$$p(\beta_j) = \frac{1}{2b} \exp\left(-\frac{|\beta_j|}{b}\right)$$

The Laplace prior concentrates mass near zero, inducing sparsity by shrinking irrelevant coefficients toward zero while leaving genuine effects largely intact.

### 3.2 Selection Criterion

A variable is retained if its **94% Highest Density Interval (HDI) excludes zero**:

$$\text{Retain if:} \quad \text{HDI}_{3\%} > 0 \quad \text{or} \quad \text{HDI}_{97\%} < 0$$

### 3.3 Results

Out of 27 candidate predictors, **3 drivers** survive the selection criterion:

| Predictor | β̄ (posterior mean) | 94% HDI | Interpretation |
|-----------|---------------------|---------|----------------|
| HDI Income | ≈ +0.033 | [0.017, 0.068] | Higher income → higher business survival |
| Distance to capital | ≈ −0.067 | excludes 0 | Greater distance → reduced viability |
| Urbanization (public streets) | ≈ +0.001 | excludes 0 | Near-zero; likely absorbed by spatial structure |

---

## 4. The BYM2 Spatial Model

### 4.1 Likelihood

Business survival is observed as active firms $y_i$ out of total firms $n_i$. To account for overdispersion inherent in count data across heterogeneous municipalities, a **Beta–Binomial** likelihood is used:

$$y_i \sim \text{BetaBinomial}\left(n_i,\ p_i \cdot \kappa + \epsilon,\ (1-p_i) \cdot \kappa + \epsilon\right)$$

where $\kappa \sim \text{HalfNormal}(50)$ controls dispersion and $\epsilon = 0.01$ ensures numerical stability.

### 4.2 Linear Predictor

$$\text{logit}(p_i) = \alpha + \mathbf{X}_i\boldsymbol{\beta} + \delta_i$$

### 4.3 Spatial Random Effect (BYM2)

The spatial component $\delta_i$ follows the **Besag–York–Mollié 2** (BYM2) parameterization (Riebler et al., 2016):

$$\delta_i = \sigma \left(\sqrt{\frac{\rho}{s}} \cdot \phi_i + \sqrt{1-\rho} \cdot \theta_i\right)$$

| Component | Description |
|-----------|-------------|
| **φ_i** (structured) | ICAR component — captures spatial spillover between neighboring municipalities |
| **θ_i** (unstructured) | IID Gaussian — captures municipality-specific noise |
| **ρ** (mixing) | Beta prior — controls fraction of variance explained by spatial structure vs. noise |
| **σ** (scale) | HalfNormal prior — overall magnitude of spatial effects |
| **s** | Scaling constant derived from the adjacency graph (ensures φ_i has unit variance) |

The BYM2 reparameterization resolves the identifiability issues of the original BYM model by introducing a global variance parameter and a mixing parameter with interpretable penalized complexity priors (Simpson et al., 2017).

### 4.4 Priors

| Parameter | Prior | Rationale |
|-----------|-------|-----------|
| α (intercept) | Normal(0, 1) | Weakly informative on logit scale |
| β_j (covariates) | Normal(0, 1) | Post-Lasso selection; regularizing |
| σ (spatial scale) | HalfNormal(1) | Penalized complexity prior |
| ρ (mixing) | Beta(0.5, 0.5) | Uniform over spatial/noise trade-off |
| κ (dispersion) | HalfNormal(50) | Accommodates overdispersion |

### 4.5 Prior Predictive Check

A prior predictive check on the linear baseline confirms that Gaussian priors on α and β, combined with the logit transformation, concentrate prior mass near $p \approx 0$ and $p \approx 1$ (U-shaped pattern). This well-known behavior of logistic models motivates the use of weakly informative priors.

---

## 5. Estimation

- **Framework:** PyMC ≥ 5.10
- **Sampler:** `pymc.sampling.jax.sample_numpyro_nuts` (JAX/NumPyro NUTS)
- **Convergence:** Monitored via R̂ — all parameters achieve R̂ ≤ 1.03

---

## 6. Diagnostics & Model Validation

### 6.1 Convergence

All monitored parameters converge with R̂ ≤ 1.03. The slightly elevated value for β[2] (R̂ = 1.03) remains within acceptable bounds (Gelman et al., 2013).

### 6.2 PSIS-LOO Cross-Validation

Predictive performance is assessed using **Pareto-Smoothed Importance Sampling LOO** (Vehtari et al., 2017):

$$\widehat{\text{elpd}}_{\text{loo}} = \sum_{i=1}^{N} \log\, p(y_i \mid y_{-i})$$

| Model | ELPD | p_loo |
|-------|------|-------|
| BYM2 (spatial) | −3,737.1 | ≈ 80.9 |
| Linear baseline | −3,766.1 | ≈ 5.2 |
| **Improvement** | **+28.6 units** | — |

Stacking weights assign essentially all predictive weight (≈1.0) to the BYM2 model.

### 6.3 Posterior Predictive Check (PPC)

Replicated datasets $\tilde{y}$ are drawn from the posterior and compared to observed data. The model successfully reproduces the empirical distribution of business survival counts.

### 6.4 Residual Spatial Autocorrelation

Moran's I is applied to normalized posterior predictive residuals $r_i = (y_i - \hat{y}_i)/n_i$ on the Queen contiguity graph:

> **Moran's I = 0.0017, permutation p-value = 0.451** — no residual spatial autocorrelation.

This confirms the BYM2 component fully absorbs the spatial structure present in the data.

### 6.5 Spatial Block K-Fold Cross-Validation

Municipalities are partitioned into geographic blocks. Key results:
- Most blocks: MAE ≈ 57–96 (low prediction error)
- More heterogeneous blocks: average MAE ≈ 163 (reflecting real spatial imbalance, not model instability)

---

## 7. Key Empirical Findings

| Finding | Value |
|---------|-------|
| Spatial mixing parameter ρ | ≈ 0.848 (HDI: [0.672, 0.993]) |
| Spatial variance share | **≈ 85%** governed by latent spatial dependence |
| Spatial scale (σ_total) | ≈ 0.067 (modest magnitude) |
| Dispersion parameter κ | ≈ 288 (limited extra-Binomial variability) |
| Prior sensitivity (Δρ) | ≈ 0.0011 (spatial dependence is data-driven) |

---

## 8. Strategic Output: Quadrant Classification

Municipalities are classified into four strategic quadrants based on **posterior success probability** and **posterior uncertainty**:

| Quadrant | Profile | Action |
|----------|---------|--------|
| 🟢 **Safe Opportunity** | High success, low uncertainty | Anchor for economic expansion |
| 🟡 **High Stakes** | High success, high uncertainty | Attractive but risk-sensitive; strong infrastructure, distant from capital |
| 🟠 **Underperformer** | Low success, low uncertainty | Structurally limited; model is confident in constraint |
| 🔴 **Critical Zone** | Low success, high uncertainty | Compounded disadvantage across income, infrastructure, and accessibility |

A **radar (spider) chart** visualizes the mean Z-scored predictor profiles for each quadrant, using only the 3 Bayesian Lasso-retained drivers.

---

## 9. Advanced Spatial Analytics

### 9.1 Latent Spatial Effect

The latent effect $\bar{\delta}_i$ isolates residual geographic variation after accounting for covariates:

$$\delta_i = \sigma \left(\sqrt{\frac{\rho}{s}} \cdot \phi_i + \sqrt{1-\rho} \cdot \theta_i\right)$$

- **Northwestern municipalities**: positive latent effects (δ_i ≈ +0.10) — outcomes exceed covariate-based expectations.
- **São Paulo metropolitan corridor**: negative latent effects (δ_i ≈ −0.15) — outcomes largely explained by covariates.

### 9.2 Bayesian Hotspot Identification

Hotspots and coldspots are classified via **posterior exceedance probabilities**:

$$P(p_i > \tau \mid \mathbf{y}) = \frac{1}{S} \sum_{s=1}^{S} \mathbf{1}\left[p_i^{(s)} > \tau\right]$$

| Category | Criterion | Count (SP) |
|----------|-----------|-----------|
| **Hotspot** | P(p_i > Q75) ≥ 0.80 | 106 (16.5%) |
| **Emerging Hotspot** | 0.60 ≤ P(p_i > Q75) < 0.80 | 36 |
| **Inconclusive** | both < 0.60 | 389 (60.4%) |
| **Emerging Coldspot** | 0.60 ≤ P(p_i < Q25) < 0.80 | 82 |
| **Coldspot** | P(p_i < Q25) ≥ 0.80 | 32 (4.7%) |

---

## 10. Domain Validation & Sensitivity

### 10.1 Sectoral Models

The BYM2 framework is replicated on sector-specific subsets: **Retail** and **Food & Beverage**. Key observations:
- Covariate effects attenuate or shift sign across sectors.
- **Spatial mixing parameter remains stable (ρ ≈ 0.86–0.89)**, confirming that the spatial mechanism is structural and not sector-dependent.
- KDE plots compare empirical vs. posterior-predicted survival distributions by sector, visually quantifying spatial shrinkage.

### 10.2 Geographic Validation — Rio Grande do Sul (N = 499)

The model is fully replicated on Rio Grande do Sul to test cross-regional stability:
- Core spatial structure is preserved across a distinct political, geographic, and economic topology.
- ρ remains consistently high, establishing the framework as generalizable.

### 10.3 Prior Sensitivity Analysis

Sensitivity of ρ to prior specification is evaluated by perturbing the Beta prior hyperparameters. The negligible drift (Δρ ≈ 0.0011) confirms that estimated spatial dependence is **data-driven, not prior-induced**.

---

## 11. Limitations

- **MAUP (Modifiable Areal Unit Problem):** Municipality-level aggregation may obscure intra-urban heterogeneity.
- **Contiguity-based adjacency:** Does not capture functional connectivity (e.g., transportation networks, supply chains).
- **Cross-sectional design:** Cannot capture temporal dynamics such as economic cycles or structural transitions.
- **Ecological inference:** Model outputs are regional-level estimates; they should not be interpreted as predictions for individual firms.

---

## 12. Future Directions

1. **Spatiotemporal extension** — Incorporating temporal dynamics to detect emerging growth corridors.
2. **Finer spatial resolution** — Moving from municipalities to census tracts to reduce aggregation bias.
3. **Functional connectivity** — Enhancing the weight structure with travel times and logistics networks.
4. **National scale** — Applying the framework to all 5,570 Brazilian municipalities.

---

## References

Anselin, L. (1995). Local indicators of spatial association — LISA. *Geographical Analysis*, 27(2), 93–115.

Besag, J., York, J., & Mollié, A. (1991). Bayesian image restoration, with two applications in spatial statistics. *Annals of the Institute of Statistical Mathematics*, 43(1), 1–20.

Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.

Riebler, A., Sørbye, S. H., Simpson, D., & Rue, H. (2016). An intuitive Bayesian spatial model for disease mapping that accounts for scaling. *Statistical Methods in Medical Research*, 25(4), 1145–1165.

Simpson, D., Rue, H., Riebler, A., Martins, T. G., & Sørbye, S. H. (2017). Penalising model component complexity: A principled, practical approach to constructing priors. *Statistical Science*, 32(1), 1–28.

Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC. *Statistics and Computing*, 27(5), 1413–1432.

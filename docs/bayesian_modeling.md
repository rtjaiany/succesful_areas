# 🧠 Bayesian Spatial Modeling & Site Selection

This document details the **i-Guide Spatial AI Framework**, which utilizes a Bayesian hierarchical approach to quantify market entry risk and business viability across geographic regions.

---

## 🎯 Strategic Relevance

Entering a new market is one of the most critical strategic decisions for firms seeking sustained growth. Global statistics suggest that nearly 50% of new ventures cease operations within their first five years (Shepard, 2024), with 35% of failures occurring because products do not meet actual market needs (CB Insights, 2021).

The **i-Guide** project addresses this by integrating spatial heterogeneity—the geographic variation in infrastructure, accessibility, and demographics—into a predictive framework. We propose a **Spatial Artificial Intelligence (Spatial AI)** framework based on a **Bayesian hierarchical spatial model** to identify geographically favorable locations for market entry.

---

## 🏛️ The 6-Pillar Evaluation Framework

To ensure scientific rigor and industrial applicability, the modeling process is structured around six key pillars:

1.  **Notebook Quality:** High-performance, reproducible MCMC sampling.
2.  **AI-Ready Data:** Multi-source integration (Census, OSM, Satellite) with quality diagnostics (VIF, Moran's I).
3.  **Novelty:** Implementation of the **BYM2 (Besag-York-Molliéri)** specification.
4.  **Storytelling:** Advanced visualization of spatial coefficients and uncertainty ranges (HDI).
5.  **Impact:** Translation of abstract priors into concrete site-selection recommendations.
6.  **FAIR & Open Science:** Adherence to open data standards and a clear future roadmap.

---

## 🔬 Methodology: The BYM2 Model

We model the business success rate using a **Binomial distribution** as the likelihood function:

$$y_i \sim \text{Binomial}(n_i, p_i)$$

Where $p_i$ (probability of success) is modeled via a logit link function that accounts for local predictors and spatial structure:

$$\text{logit}(p_i) = \alpha + \mathbf{X}_i \beta + \sigma (\sqrt{\rho} \cdot \phi_i + \sqrt{1-\rho} \cdot \theta_i)$$

### Components of the Spatial Effect:
-   **$\phi_i$ (Structured):** Intrinsic Conditional Autoregressive (ICAR) component capturing regional spillover effects.
-   **$\theta_i$ (Unstructured):** IID Gaussian random effects capturing municipality-specific noise.
-   **$\rho$ (Mixing Parameter):** A Beta prior manages the balance between spatial structure and local variance.

---

## 🛠️ Implementation Details

-   **Framework:** PyMC 5.10+
-   **Computation:** JAX/NumPyro for high-performance parallel sampling.
-   **Spatial Weights:** Queen adjacency matrix with island handling.
-   **Diagnostics:** Global Moran's I to confirm spatial clustering and VIF to prevent multicollinearity.

### Advanced Diagnostics & Verification
We monitor model complexity, spatial shrinkage, and potential overfitting using a comprehensive suite of diagnostics:
-   **PSIS-LOO (Location-One-Out) CV:** Estimating out-of-sample predictive accuracy robustly.
-   **Posterior Predictive Checks (PPC):** Comparing observed success counts vs. model-simulated success counts to ensure empirical validity.
-   **Spatial K-Fold Cross-Validation:** Validating spatial dependence across administrative domains.
-   **Shrinkage and Residual Metrics:** Advanced evaluation of how much spatial smoothing is occurring versus how much variance is driven by residuals.
-   **R-hat Diagnostics:** Ensuring convergence across multiple JAX-accelerated MCMC chains.

---

## 📈 Sectoral Specificity & Sensitivity

Recent model iterations introduce capabilities to visualize and measure how different economic micro-sectors react to spatial realities.
-   **Subpopulation Sensitivity Analysis:** The modeling framework supports testing robustness across granular market sub-divisions, providing Ph.D.-level scrutiny of sub-demographics.
-   **KDE Visualizations for Spatial Shrinkage:** Comparing the empirical reality against spatially-smoothed Bayesian posterior predictions. Specific focus is placed on dissecting baseline divergence for the **Retail** and **Food & Beverage** sectors through Kernel Density Estimation (KDE) plots.

---

## 🏁 Next Steps & Roadmap
1.  **National Implementation:** Scaling the Bayesian model to test and implement across all of **Brazil** (5,570 municipalities).
2.  **Cross-Regional Validation:** Testing model stability across diverse cultural and economic regions with national-scale data.
3.  **Hierarchical Structural Testing:** Analyzing model performance along nested layers (**cities, states, and regions**) to capture administrative variance.
4.  **Sectoral Specificity:** Move beyond aggregated metrics to test specific **Economic Sectors** (Retail, Industry, Services, etc.).

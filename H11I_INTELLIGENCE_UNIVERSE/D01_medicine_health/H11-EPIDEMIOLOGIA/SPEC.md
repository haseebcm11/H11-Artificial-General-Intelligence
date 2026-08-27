> **Layer 1** · Medicine & Health Sciences · `H11-EPIDEMIOLOGIA`

## Purpose
The `H11-EPIDEMIOLOGIA` agent provides multi-scale computational modeling of infectious and chronic disease transmission dynamics, spatiotemporal outbreak forecasting, contact network structures, intervention optimization (non-pharmaceutical and pharmaceutical), and causal risk stratification across populations.

It serves as the core population-level epidemiological engine for the H11 cognitive substrate, bridging micro-level pathogen biology (from `H11-VIROLOGIA` and `H11-BACTERIOLOGIA`) with macroeconomic, clinical surge, and public health policy layers.

## Technical Deep-Dive
The agent couples compartmental ODE systems with stochastic metapopulation networks and empirical statistical renewal methods:

1. **Stratified Compartmental Dynamics (SEIRD/SEIRS):**
   Models transmission across age-stratified cohorts and metapopulation geographic patches using high-order numerical integration (Runge-Kutta 4th order). Incorporates contact mixing matrices $C_{ij}$ (e.g., POLYMOD/Wallinga frameworks), age-dependent susceptibility, asymptomatic transmission fractions ($\theta$), latent incubation delays, and waning humoral immunity:
   $$\frac{dS_i}{dt} = -\beta S_i \sum_{j} C_{ij} \frac{I_j + \theta A_j}{N_j} + \omega R_i$$
   $$\frac{dE_i}{dt} = \beta S_i \sum_{j} C_{ij} \frac{I_j + \theta A_j}{N_j} - \sigma E_i$$
   $$\frac{dI_i}{dt} = (1 - p_{\text{asymp}}) \sigma E_i - \gamma I_i - \mu_i I_i$$
   $$\frac{dA_i}{dt} = p_{\text{asymp}} \sigma E_i - \gamma_A A_i$$
   $$\frac{dR_i}{dt} = \gamma I_i + \gamma_A A_i - \omega R_i$$
   $$\frac{dD_i}{dt} = \mu_i I_i$$

2. **Real-Time Reproduction Number ($R_t$) Renewal Estimation:**
   Implements the Cori et al. Bayesian renewal equation framework to compute instantaneous reproduction numbers $R_t$ from incidence time series $I_t$ and discretized serial interval distributions $w_s \sim \text{Gamma}(\mu, \sigma^2)$:
   $$R_t = \frac{I_t}{\sum_{s=1}^t I_{t-s} w_s}$$
   Evaluates sliding time windows ($\tau$) with analytical Gamma posterior distributions to yield exact 95% credible intervals.

3. **Metapopulation Network & Spatial Mobility:**
   Integrates gravity and radiation mobility formulations across interconnected regional nodes, computing inter-patch infection seeding based on commuter flows, transit networks, and distance-decay functions.

4. **Intervention Modeling (NPIs & PIs):**
   Evaluates dynamic non-pharmaceutical interventions (social distancing, school/workplace closures, mask adherence, isolation latency) and vaccination campaigns (ring vaccination, targeted age rollouts, breakthrough infection parameters, critical vaccination coverage thresholds $V_c = \frac{1 - 1/R_0}{E_{\text{vaccine}}}$).

5. **Causal Risk & Observational Analytics:**
   Computes epidemiological effect measures including Risk Ratios (RR), Odds Ratios (OR), Attributable Risk (AR), Population Attributable Fractions (PAF), and Mantel-Haenszel stratified confounding adjustments.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `pathogen_profile` | `PathogenProfile` | Biological parameters including $R_0$, incubation period, infectious duration, and serial interval. |
| `population_patches` | `List[MetapopulationPatch]` | Spatial regions with census populations, demographic cohorts, and spatial coordinates. |
| `incidence_time_series` | `List[int]` | Daily observed case counts for real-time renewal analysis. |
| `active_interventions` | `List[Intervention]` | Scheduled or active policy measures (NPIs, vaccination schedules). |
| `mobility_matrix` | `Matrix[N, N]` | Symmetric or asymmetric inter-patch daily commuter fractions. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `compartment_trajectories` | `Dict[str, List[CompartmentState]]` | Day-by-day simulated counts for S, E, I, A, R, D compartments across all patches. |
| `rt_trajectory` | `List[RtEstimate]` | Time-series of point estimates and 95% Bayesian credible intervals for $R_t$. |
| `epidemic_peaks` | `Dict[str, PeakMetric]` | Projected peak dates, active case load at peak, and ICU capacity threshold crossings. |
| `intervention_impact` | `InterventionImpactSummary` | Averted infections, averted fatalities, and effective transmission reduction percentage. |
| `causal_risk_metrics` | `CausalRiskProfile` | Odds ratios, relative risks, and population attributable fractions for exposure cohorts. |

### State Schema
Maintains `EpidemiologicalState` tracking active transmission clusters, aggregate seroprevalence, cumulative mortality, current effective reproduction number, and active intervention policies.

## Dependencies
### Upstream (depends on)
- `H11-VIROLOGIA`: Pathogen viral load kinetics, mutation drift rates, and immune escape phenotypes.
- `H11-BACTERIOLOGIA`: Bacterial virulence determinants, carrier states, and antimicrobial resistance profiles.
- `H11-HEALTHINFORMATICA`: Electronic health records, syndromic surveillance streams, and laboratory test reporting.

### Downstream (feeds into)
- `H11-HEALTHINFORMATICA`: Public health alerting, syndromic anomaly alerts, and outbreak dashboards.
- `H11-IMMUNOTHERAPIA`: Target population sizing for monoclonal antibodies and targeted vaccine deployment.
- `H11-PNEUMOLOGIA` / `H11-CARDIOLOGIA`: Hospitalization surge forecasts and post-infectious sequelae burden modeling.
- `H11-PALLIATIVA`: Critical mortality forecasts and palliative resource allocation planning.

## Failure Modes
1. **Reporting Truncation & Lag Inversion:** Uncorrected reporting delays in syndromic reporting leading to erroneous downward bias in recent $R_t$ estimates.
2. **Homogeneous Mixing Fallacy:** Assuming uniform population contact leading to severe overestimation of epidemic attack rates in superspreader-driven pathogens ($k < 0.1$).
3. **Identifiability Degeneracy:** Simultaneous co-estimation of reporting rates and transmission probability under sparse serosurvey data yielding multiple mathematical equilibria.
4. **Boundary Condition Overflow:** Neglecting boundary importations from external international travel reservoirs during local eradication phases.

## Performance Characteristics
- Instantaneous renewal $R_t$ estimation for a 365-day incidence series: <3 ms.
- High-order 4-stage Runge-Kutta simulation of a 50-patch stratified SEIRD model over 365 days: <85 ms.
- Memory footprint: ~12 MB baseline state; linear $O(N \cdot T)$ scaling with patches $N$ and simulated timesteps $T$.

## Research References
1. Cori, A., Ferguson, N. M., Fraser, C., & Cauchemez, S. (2013). *A new framework and software to estimate time-varying reproduction numbers during epidemics*. American Journal of Epidemiology, 178(9), 1505-1512.
2. Anderson, R. M., & May, R. M. (1992). *Infectious Diseases of Humans: Dynamics and Control*. Oxford University Press.
3. Wallinga, J., & Teunis, P. (2004). *Different epidemic curves for severe acute respiratory syndrome reveal similar impacts of control measures*. American Journal of Epidemiology, 160(6), 509-516.
4. Mossong, J., et al. (2008). *Social contacts and mixing patterns for infectious disease transmission*. PLOS Medicine, 5(3), e74.

## Implementation Notes
- Uses Runge-Kutta 4th order ODE integration with sub-stepping for numerical stability during rapid exponential growth phases.
- Implements gamma-distributed discretization of serial intervals with normalization over truncation windows.
- Provides statistical confidence limits for epidemiological causal association metrics (Wald log-normal approximation).

> **Layer 1** · Medicine & Health Sciences · `H11-GLOBALHEALTH`

## Purpose
The H11-GLOBALHEALTH agent models, quantifies, and orchestrates transnational health dynamics across multi-scale populations. It assesses the Global Burden of Disease (GBD) via Disability-Adjusted Life Years (DALYs), conducts cross-border infectious threat surveillance in accordance with the International Health Regulations (IHR), evaluates Universal Health Coverage (UHC) service capacity, optimizes equitable resource/vaccine allocation under scarcity, and models climate-induced planetary health vulnerabilities.

## Technical Deep-Dive
The agent operates at the intersection of international epidemiology, health economics, planetary health, and health system resilience engineering:

1. **Global Burden of Disease (GBD) Analytics**:
   Computes comprehensive disease burden using standard DALY formulations:
   $$\text{DALY} = \text{YLL} + \text{YLD}$$
   $$\text{YLL} = \sum_{a} d_a \times e_a^*, \quad \text{YLD} = \sum_{a} I_a \times DW \times L_a$$
   where $d_a$ is deaths at age $a$, $e_a^*$ is standard life expectancy at age $a$, $I_a$ is incident cases, $DW$ is disability weight ($0.0 \le DW \le 1.0$), and $L_a$ is average duration of disability.

2. **Cross-Border Pathogen Importation Hazard**:
   Simulates metapopulation infectious dispersal across international civil aviation and land migration networks. Computes importation risk $\mathcal{R}_{\text{imp}}$ based on origin pathogen prevalence, outbound flow velocity, transmission serial interval, and destination border detection efficacy.

3. **Universal Health Coverage (UHC) & Financial Protection**:
   Evaluates the WHO UHC Service Coverage Index (SDG 3.8.1) spanning infectious diseases, non-communicable diseases (NCDs), maternal/child health, and service capacity, matched against catastrophic health spending thresholds (SDG 3.8.2).

4. **Equity-Constrained Vaccine & Countermeasure Allocation**:
   Implements multi-objective welfare optimization (utilitarian-prioritarian blends akin to Gavi/COVAX Fair Allocation Framework) prioritizing vulnerable demographics, healthcare workforce density, and local CFR (case fatality rate) surges under cold-chain supply chain constraints.

5. **Planetary Health & Climate Vector Shifts**:
   Computes temperature-precipitation-humidity suitability indices for vector-borne arboviruses (*Aedes aegypti*, *Anopheles gambiae*) and models heat-mortality risk functions across changing planetary microclimates.

6. **One Health Transboundary Surveillance**:
   Ingests zoonotic spillover signals, livestock antimicrobial resistance (AMR) indices, and human-wildlife interface exposures to identify pre-pandemic emergence events.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `country_iso` | `str` | ISO 3166-1 alpha-3 territory code |
| `demographics` | `CountryDemographics` | Age-stratified population, birth rate, baseline life expectancy |
| `disease_burden_input` | `DiseaseBurdenInput` | Cause-specific mortality, incidence, disability weight ($DW$), duration |
| `health_capacity` | `HealthSystemCapacity` | Physicians/nurses per 10k, ICU beds, oxygen surge, cold chain integrity |
| `mobility_links` | `List[MobilityLink]` | Transnational passenger origin-destination matrices |
| `climate_covariates` | `ClimateHealthCovariates` | Temperature anomaly, relative humidity, precipitation, wet-bulb metrics |
| `surveillance_signals` | `List[OneHealthRecord]` | Zoonotic events, environmental pathogen detections, AMR isolates |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `daly_breakdown` | `DALYBreakdown` | Granular YLL, YLD, total DALYs, and rate per 100,000 population |
| `uhc_coverage_index` | `Dict[str, float]` | 0-100 composite index and catastrophic expenditure hazard |
| `importation_hazard_score` | `float` | Probability index ($0.0-1.0$) of pathogen importation within $T$ days |
| `resource_allocation` | `List[VaccineAllocationResult]` | Optimized distribution schedule by equity and logistics constraints |
| `vector_suitability_index` | `float` | Vectorial capacity coefficient for climate-sensitive pathogens |
| `global_health_alerts` | `List[GlobalHealthAlert]` | Actionable early warnings for transboundary spillover or collapse |

### State Schema
Maintains a distributed sovereign country profile registry (`CountryDemographics`, `HealthSystemCapacity`), a directed transboundary mobility and hazard graph, and an active AMR / One Health surveillance log.

## Dependencies

### Upstream (depends on)
- `H11-EPIDEMIOLOGIA`: R0, generation intervals, transmission dynamics.
- `H11-VIROLOGIA`: Pathogen viral clade characteristics, immune escape potential.
- `H11-HEALTHINFORMATICA`: Standardized global EHR and mortality reporting feeds.
- `D04_earth_planetary`: Planetary climate, temperature anomalies, extreme weather forecasts.

### Downstream (feeds into)
- `H11-PUBLICHEALTH`: National and subnational disease prevention, local non-pharmaceutical interventions.
- `H11-IMMUNOLOGIA`: Vaccine target population prioritization and antigen design requirements.
- `D07_governance_policy`: International health regulation compliance, emergency declarations, treaty negotiation briefs.

## Failure Modes
1. **Reporting Asymmetry & Lag**: Severe underreporting or political suppression of case counts in data-scarce settings resulting in underestimated importation hazards.
2. **Disability Weight Miscalibration**: Outdated or culturally non-representative disability weights ($DW$) skewing burden priorities away from neglected tropical diseases (NTDs) or mental health.
3. **Logistics & Cold-Chain Over-Optimism**: Allocating mRNA/ultracold biologicals to regions lacking continuous $-80^\circ\text{C}$ infrastructure without adjusting for spoilage wastage.
4. **Climate Covariate Extrapolation Drift**: Vector suitability models failing under unprecedented microclimatic extremes.

## Performance Characteristics
- Multi-country global burden recalculation (195 territories): $< 350\text{ ms}$.
- Cross-border transmission network diffusion step: $< 50\text{ ms}$ for $10^4$ flight routes.
- Memory footprint: $< 256\text{ MB}$ state cache for global territorial profiles and historical GBD time-series.

## Research References
- Murray, C. J., & Lopez, A. D. *The Global Burden of Disease: A comprehensive assessment of mortality and disability from diseases, injuries, and risk factors in 1990 and projected to 2020*. WHO/Harvard.
- World Health Organization. *International Health Regulations (2005)*. 3rd Edition.
- Whitmee, S., et al. *Safeguarding human health in the Anthropocene epoch: report of The Rockefeller Foundation–Lancet Commission on planetary health*. The Lancet, 2015.
- Gavi, the Vaccine Alliance. *COVAX Global Equitable Access and Allocation Mechanism*.

## Implementation Notes
Employs vectorized DALY calculators with standard WHO reference life tables, priority-weighted constrained linear resource allocation algorithms, and non-linear vectorial capacity functions based on temperature-dependent EIP (extrinsic incubation period) and mosquito mortality kinetics.

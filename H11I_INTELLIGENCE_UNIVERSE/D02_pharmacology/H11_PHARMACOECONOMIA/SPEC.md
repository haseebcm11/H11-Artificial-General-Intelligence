# H11-PHARMACOECONOMIA: Pharmacoeconomics Agent

## Overview
The H11-PHARMACOECONOMIA agent evaluates the economic viability, cost-effectiveness, and budget impact of pharmacological interventions and health technologies. It employs Markov modeling, decision trees, and Monte Carlo simulations to estimate Quality-Adjusted Life Years (QALYs), Incremental Cost-Effectiveness Ratios (ICERs), and overall healthcare budget impacts.

## Architecture
The agent is built on three foundational modules:
1.  **Cost-Utility Analysis Engine**: Calculates QALYs and ICERs using time-horizon probabilistic models.
2.  **Markov Modeling System**: Simulates patient transitions through health states over time.
3.  **Budget Impact Assessor**: Determines short-to-medium term financial impacts on specific payer systems, incorporating market share, population size, and displacement of existing therapies.

## Interfaces
- Input: `HealthEconomicsQuery` encompassing intervention costs, standard-of-care costs, transition probabilities, and utility weights.
- Output: `PharmacoeconomicReport` detailing expected costs, ICER, acceptability curves, and sensitivity analysis results.

## Algorithms
- **Probabilistic Sensitivity Analysis (PSA)**: Uses Dirichlet distributions for transition probabilities and Beta distributions for utilities.
- **Half-Cycle Correction**: Applied to Markov models to adjust for continuous transitions over discrete cycles.
- **Willingness-To-Pay (WTP) Thresholding**: Determines cost-effectiveness probability based on standard thresholds (e.g., $50,000 to $150,000 per QALY).

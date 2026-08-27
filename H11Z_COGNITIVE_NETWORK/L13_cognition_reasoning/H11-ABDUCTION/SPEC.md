# H11-ABDUCTION: Abductive Reasoning Agent

## Overview
The H11-ABDUCTION agent performs "inference to the best explanation" (IBE). Given a set of observations (manifestations) and a domain theory connecting causes (hypotheses) to effects, the agent generates the most plausible explanatory hypothesis.

## Theoretical Foundations
- **Set-Covering Abduction**: Formulated by Peng & Reggia. The goal is to find a minimal set of hypotheses that together can cause all observed manifestations.
- **Parsimony**: Ockham's Razor is applied such that simpler, less contrived hypothesis sets are preferred over complex ones.
- **Bayesian Abduction**: Using priors and likelihoods to score the probabilistically most likely explanation.

## Architecture
1. **Hypothesis Generator**: Uses inverted causal rules to generate candidate causes for each observation.
2. **Set-Covering Solver**: Finds combinations of causes that cover all observations.
3. **Parsimony Evaluator**: Ranks covering sets based on minimality (cardinality) and prior probability.

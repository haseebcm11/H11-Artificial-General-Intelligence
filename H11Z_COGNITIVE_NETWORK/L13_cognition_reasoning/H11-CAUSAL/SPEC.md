# H11-CAUSAL Specification

## Overview
H11-CAUSAL implements causal inference and reasoning capabilities. It utilizes Structural Causal Models (SCMs), directed acyclic graphs (DAGs), and Pearl's do-calculus to transition from associative (correlation) to interventionist (causation) logic. 

## Core Capabilities
- **Causal Discovery**: Identifying cause-effect relationships from data/knowledge.
- **Intervention (Do-Calculus)**: Simulating the effect of actions ($P(Y | do(X))$) using backdoor and frontdoor criteria.
- **Structural Causal Models (SCMs)**: Defining equations that govern the endogenous variables based on exogenous noise and parent variables.
- **Confounding Adjustment**: Computing unbiased causal effects by adjusting for covariates.

## Theoretical Foundations
- **Pearl's Hierarchy of Causation**: 
  1. Association (Seeing): $P(Y | X)$
  2. Intervention (Doing): $P(Y | do(X))$
  3. Counterfactuals (Imagining): $P(Y_{X=x} | X=x')$ - *Handled primarily in H11-COUNTERFACTUAL*
- **Rubin Causal Model (Potential Outcomes)**: ATE, ATT, ATC estimation.
- **d-Separation**: Determining conditional independencies in DAGs.

## Architecture
- `CausalGraph`: Manages nodes, edges, and causal paths.
- `SCM`: Encapsulates structural equations and noise distributions.
- `InterventionEngine`: Computes $P(Y|do(X))$ using graphical criteria.

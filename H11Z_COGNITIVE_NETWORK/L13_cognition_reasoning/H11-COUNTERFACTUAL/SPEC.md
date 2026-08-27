# H11-COUNTERFACTUAL Specification

## Overview
H11-COUNTERFACTUAL is responsible for reasoning about alternate realities and "what-if" scenarios. It operates at the third level of Pearl's Causal Hierarchy: imagining. This agent is crucial for answering retrospective questions, assessing regret, and determining responsibility or fairness.

## Core Capabilities
- **Counterfactual Generation**: Computing $P(Y_{X=x} | E=e)$, the probability of outcome Y under intervention X=x, given that evidence E=e was observed.
- **Three-Step Counterfactual Algorithm (Pearl)**:
  1. *Abduction*: Update the probability of exogenous noise variables (U) given observed evidence E=e.
  2. *Action*: Modify the SCM by replacing the equations for the intervened variables X with constants x.
  3. *Prediction*: Compute the new probabilities of the target variables Y using the modified model and updated U.
- **Counterfactual Regret Minimization (CFR)**: For decision-making in imperfect information games.
- **Lewis Closest Worlds**: Semantics for evaluating counterfactual conditionals.

## Architecture
- `StructuralEquationModel`: Evaluates deterministic or probabilistic equations.
- `AbductionEngine`: Infers latent state given observation.
- `CounterfactualPredictor`: Modifies the SCM and rolls forward the state.

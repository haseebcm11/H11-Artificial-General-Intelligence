# H11-DECISION

## Overview
The Decision-making substrate for the H11 Cognitive Architecture. It provides a formal framework for both single-step and sequential decision-making paradigms.

## Capabilities
1. **Multi-Criteria Decision Analysis (MCDA)**: Employs the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) algorithm to rank multidimensional alternatives based on conflicting criteria.
2. **Sequential Decision Making (MDP)**: Provides a Markov Decision Process solver utilizing value iteration to derive optimal policies under stochastic environments.
3. **Risk-Aware Utility Evaluation**: Transforms expected values into expected utilities based on varying risk profiles (averse, neutral, seeking) via parameterized utility functions.

## Components
- `MCDAEngine`: Computes ideal and anti-ideal vectors, normalizes criteria, and computes relative closeness.
- `MDPEngine`: Evaluates Bellman equations to iteratively converge on an optimal value function and policy.
- `UtilityEvaluator`: Applies concave, convex, or linear transformations to lottery outcomes to compute expected utility.

# H11-INDUCTION: Inductive Reasoning Agent

## Overview
The H11-INDUCTION agent is responsible for inductive reasoning: recognizing patterns, generalizing from specific examples, and forming hypotheses that cover given data. It is inspired by Inductive Logic Programming (ILP) and sequential covering algorithms like FOIL.

## Architecture
1. **Rule Generator**: Proposes new literals to specialize current rules.
2. **Evaluator**: Evaluates the information gain of potential rule additions against positive and negative examples.
3. **Hypothesis Assembly**: Iteratively constructs a set of rules (a theory) that maximizes coverage of positive examples while minimizing coverage of negative examples.

## Key Concepts
- **Inductive Bias**: The set of assumptions the learner uses to predict outputs given inputs it has not encountered. We use a preference for shorter rules (Occam's razor).
- **Sequential Covering**: Learning one rule at a time, removing covered positive examples, and repeating.
- **Information Gain**: A metric to guide the search for rule components, maximizing the discriminative power between positive and negative instances.

# H11-EVALUATE-COG: Cognitive Evaluation Agent

## Overview
The H11-EVALUATE-COG agent provides rigorous self-assessment and verification for generated outputs. It acts as a critical meta-cognitive monitor, scoring answers, checking formal proofs, running heuristic code tests, and calibrating confidence levels before final commitment.

## Core Capabilities
- **Rubric-Based Evaluation**: Maps outputs against predefined or dynamically generated criteria matrices.
- **Verification & Proof Checking**: Validates logical consistency in reasoning chains and mathematical steps.
- **Calibrated Confidence**: Adjusts confidence scores based on the density of evidence and presence of contradictions.
- **Comparative Evaluation**: Scores multiple candidate solutions to select the optimal approach.

## Theoretical Foundations
- **Self-Reflective Agents**: Shinn et al. (2023) - Reflexion framework for language agents.
- **Calibration in LLMs**: Measuring expected accuracy vs model confidence.
- **Automated Grading & Verification**: Exact match, fuzzy match, and static analysis techniques.

## Architecture
- `EvaluationRubric`: Defines dimensions, weights, and scoring scales.
- `ConfidenceCalibrator`: Computes calibrated probabilities.
- `CognitiveEvaluator`: Coordinates the evaluation pipeline and generates structured feedback.

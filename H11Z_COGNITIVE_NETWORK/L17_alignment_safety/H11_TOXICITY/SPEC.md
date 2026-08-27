# H11-TOXICITY: Multi-dimensional Toxicity Filtering

## Overview
H11-TOXICITY is responsible for the nuanced detection of hate speech, harassment, self-harm promotion, and other harmful discourse. Unlike generic filters, it employs contextual intent analysis using transformer ensembles to prevent false positives while capturing subtle, implicit toxicity.

## Core Mechanisms
1. **Multi-Axis Scoring**: Computes independent scores for axes such as Insult, Profanity, Threat, and Microaggressions.
2. **Context Window Expansion**: Evaluates toxicity not just on a per-sentence basis, but across the conversational history to catch cumulative toxicity.
3. **Ensemble Detection**: Combines fast n-gram heuristics with deep transformer-based classifiers.

## Interfaces
- `analyze_utterance(text, context_history)`
- `compute_ensemble_score()`
- `get_toxicity_breakdown()`

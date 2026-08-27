# H11-METACOGNITION Specification

## Overview
H11-METACOGNITION is responsible for "thinking about thinking." It provides higher-order cognitive control, regulating cognitive resources, selecting problem-solving strategies, and estimating uncertainty. It enables the agent to know what it doesn't know.

## Core Capabilities
- **Confidence Estimation**: Calibrating confidence scores for generated answers.
- **Uncertainty Quantification**: Distinguishing between aleatoric (statistical noise) and epistemic (lack of knowledge) uncertainty.
- **Strategy Selection**: Dynamically choosing between fast heuristics (System 1) and slow, deliberate reasoning (System 2, e.g., Chain-of-Thought or Tree-of-Thoughts) based on task complexity.
- **Cognitive Monitoring**: Tracking resource usage (token counts, depth of search) and intervening when stuck in a loop.

## Architecture
- `UncertaintyEstimator`: Calculates entropy or confidence from token probabilities or ensemble outputs.
- `MetaController`: Routes tasks to the appropriate reasoning strategies based on estimated difficulty.
- `CognitiveMonitor`: Maintains state about the current reasoning process.

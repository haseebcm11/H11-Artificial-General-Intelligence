# H11-FOCUS: Attention Focus & Salience

## Overview
H11-FOCUS implements cognitive attention mechanisms, managing both goal-directed (top-down) and stimulus-driven (bottom-up) attention. It addresses the attentional bottleneck by selecting the most salient information for further cognitive processing, enabling selective and sustained attention.

## Core Mechanisms
1. **Salience Detection**: Computes the prominence of stimuli based on contrast, novelty, and relevance to current goals.
2. **Selective Attention**: Filters out distractors and focuses processing resources on high-salience targets.
3. **Divided Attention**: Manages resource allocation across multiple simultaneous tasks, degrading performance gracefully when overloaded.
4. **Attentional Bottleneck**: Imposes a capacity limit on working memory and cognitive processing (e.g., Global Workspace Theory).
5. **Goal-directed vs. Stimulus-driven**: Balances between voluntary focus and involuntary distraction (interruptions).

## Algorithms
- Visual Saliency Maps (Itti, Koch, & Niebur, 1998) - abstracted for cognitive states.
- Resource Allocation Models (Kahneman's Capacity Model).

## Dependencies
- NumPy
- H11 Cognitive Substrate Integration

# H11-CURIOSITY: Curiosity Drive

## Overview
H11-CURIOSITY implements exploration motivation through mechanisms such as information gain, surprise-based exploration, novelty seeking, and epistemic curiosity. It is designed to evaluate intrinsic motivation to drive the learning process and exploration-exploitation balance.

## Core Mechanisms
1. **Prediction Error (Surprise-based Exploration)**: Uses prediction error as a surrogate for intrinsic reward (e.g., as conceptualized by Schmidhuber, 1991). High prediction error indicates highly surprising states, motivating exploration.
2. **Information Gain**: Calculates the reduction in uncertainty about the environment's dynamics, guiding epistemic curiosity.
3. **Novelty Seeking**: Measures the rarity of observed states or concepts using an episodic memory buffer and density estimation.
4. **Question Generation**: Translates intrinsic motivation into explicit epistemic queries to seek knowledge actively.

## Algorithms
- **Random Network Distillation (RND)**: Used for novelty detection by predicting the output of a fixed random network.
- **Intrinsic Motivation formulations**: $r_i = \eta \| f(s_t, a_t) - s_{t+1} \|^2$ (Prediction Error).

## Dependencies
- NumPy, PyTorch (optional for deep models, numpy used for baselines)
- H11 Cognitive Memory Substrate

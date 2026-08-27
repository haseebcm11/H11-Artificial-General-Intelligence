# H11-BIAS Specification

## Overview
The H11-BIAS agent manages and regulates bias parameters throughout the network. It incorporates mechanisms for dynamic bias shifting, handling inductive biases inherently tied to network topology, and adjusting biases in conjunction with normalization layers (like Batch Norm folding).

## Core Capabilities
1. **Bias Initialization**: Smart initializations for biases (e.g., setting biases to positive values to avoid dead ReLUs).
2. **Covariate Shift Management**: Adjusting moving averages and compensating for internal covariate shift.
3. **Inductive Biases**: Structural and parameterized regularizers that encourage certain transformations.

## Architecture
- `BiasTracker`: Maintains running statistics of layer activations to dynamically adapt biases.
- `FoldingEngine`: Folds batch norm statistics into biases for inference speedup.

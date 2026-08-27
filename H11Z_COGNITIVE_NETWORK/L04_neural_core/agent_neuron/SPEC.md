# H11-NEURON Specification

## Overview
The H11-NEURON agent is responsible for modeling and simulating artificial neurons within the H11 cognitive substrate. It covers classic models (McCulloch-Pitts, perceptrons) as well as modern continuous differentiable variants with gradient tracking.

## Core Capabilities
1. **Neuron Modeling**: Supports configuration of distinct neuron archetypes including threshold logic units, continuous differentiable nodes, and spiking approximations.
2. **Gradient Tracking**: Accumulates local gradients for backpropagation-through-time (BPTT) and real-time recurrent learning (RTRL).
3. **State Management**: Maintains historical membrane potentials or activation histories for use in temporal credit assignment.

## Architecture
- `NeuronState`: Represents the instantaneous voltage, firing threshold, and refractory period of a neuron.
- `GradientBuffer`: Caches partial derivatives for upstream layer consumption.
- `UpdateMechanics`: Governs how inputs are aggregated (summation, multiplicative integration) before activation.

## Interfaces
- **Input**: Synaptic currents and bias offsets.
- **Output**: Firing rates, spike trains, or continuous activations.

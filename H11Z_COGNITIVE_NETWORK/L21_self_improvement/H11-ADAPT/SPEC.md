# H11-ADAPT Specification

## Overview
The H11-ADAPT agent manages the online adaptation and continual learning processes of the system. It is designed to mitigate catastrophic forgetting when the agent encounters non-stationary data distributions in real-time.

## Core Algorithms
1. **Elastic Weight Consolidation (EWC)**: Computes the Fisher Information Matrix to identify and protect critical parameters of past tasks.
2. **Distribution Shift Detection**: Uses Maximum Mean Discrepancy (MMD) to detect when the incoming data distribution has drifted significantly from the historical baseline.
3. **Experience Replay Buffer**: Maintains a reservoir-sampled memory of diverse past experiences to interleave with new data during online updates.

## Interfaces
- **Input**: Streaming data batches, current model state.
- **Output**: Shift detection alerts, consolidated weights, replay samples.

## Data Structures
- `ReplayMemory`: A cyclic buffer implementing reservoir sampling.
- `FisherDiagonal`: The diagonal approximation of the Fisher Information Matrix.
- `ShiftMetric`: Dataclass containing MMD scores and p-values.

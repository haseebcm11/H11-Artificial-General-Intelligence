> **Layer 23** · Energy, Thermal & Sustainability · `H11-EFFICIENCY`

## Purpose

The H11-EFFICIENCY agent measures, analyzes, and optimizes the computational efficiency of models running on the H11 substrate. It bridges the gap between software design (model architecture) and hardware execution (energy consumed), focusing on metrics like FLOPs-per-watt and tokens-per-joule.

## Technical Deep-Dive

This agent instruments PyTorch and XLA execution graphs to correlate kernel-level execution with precise energy readings. It models the Roofline performance of the hardware under various precision formats (FP8, INT4, BF16) and identifies memory-bound versus compute-bound phases. By quantifying the energy cost of memory transactions versus ALU operations, it provides actionable feedback for model quantization and sparsity application.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `kernel_traces` | `ExecutionTrace` | Timestamps and ops for executed kernels |
| `power_trace` | `PowerTrace` | High-frequency power samples during execution |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `efficiency_report` | `EfficiencyMetrics` | Tokens/Joule and FLOPs/Watt stats |
| `optimization_hints` | `List[Optimization]` | Recommendations (e.g., 'increase batch size') |

### State Schema
Maintains a baseline registry of known architectures (e.g., standard Llama-3, Mixture of Experts) and their empirical efficiency frontiers.

## Dependencies
- H11-ENERGY: Provides granular power traces.
- H11-INFERENCE (L7): Provides kernel traces.

## Failure Modes
1. Trace Misalignment: Clock drift between software traces and hardware PDU sampling leads to invalid energy-per-token metrics.

## Performance Characteristics
Runs as an offline or low-frequency background analyzer, batch processing trace data.

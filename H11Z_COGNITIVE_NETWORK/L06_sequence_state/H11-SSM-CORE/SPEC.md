> **Layer 6** · Sequence & State-Space Engine · `H11-SSM-CORE`

## Purpose

The H11-SSM-CORE agent implements continuous-time selective state space models (e.g., Mamba, S4) natively within the substrate. It is responsible for mapping 1D sequences through implicit continuous representations using discretization (Zero-Order Hold), allowing long-range dependencies with linear time complexity compared to quadratic attention.

## Technical Deep-Dive

This agent maintains the dynamic evolution of the state vector $h_t$ based on the input $x_t$ through the discretized matrices $ar{A}, ar{B}, ar{C}$. Uniquely, it utilizes *input-dependent* selection mechanisms, where parameters $B, C,$ and $\Delta$ are functions of $x_t$, allowing the model to selectively forget or remember information dynamically—solving the historical weakness of LTI (Linear Time-Invariant) SSMs.

It handles the complex continuous-to-discrete conversion routines natively, maintaining diagonalized or block-diagonalized state spaces for extreme hardware efficiency. The agent orchestrates these computations in a parameter-efficient state dimension (e.g., N=16), expanded across the embedding dimension (D).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| hidden_states | List[List[float]] | Input sequences |
| dt_proj | List[List[float]] | Step size projection |
| state_reset | bool | Whether to flush hidden state $h_t$ |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ssm_outputs | List[List[float]] | Filtered output |
| final_state | List[float] | $h_T$ for autoregressive continuation |

### State Schema
Maintains internal hidden state arrays $h \in \mathbb{R}^{B 	imes D 	imes N}$ across forward passes for streaming capability.

## Dependencies

### Upstream (depends on)
H11-SEQUENCE

### Downstream (feeds into)
H11-SCAN

## Failure Modes
- DiscretizationInstability: NaN propagation when $\Delta$ values diverge.
- SelectionCollapse: When selective gates saturate, causing the SSM to act as a trivial LTI system.

## Performance Characteristics
Extreme linear throughput. Bound by memory bandwidth in recurrent mode; highly parallel in convolution/scan mode.

## Research References
- Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao)
- Efficiently Modeling Long Sequences with Structured State Spaces (S4)

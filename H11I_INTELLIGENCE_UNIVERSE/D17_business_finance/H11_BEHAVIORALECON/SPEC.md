> **Layer 17** · Business, Finance & Economics · `H11-BEHAVIORALECON`

## Purpose

Models bounded rationality, cognitive biases, and heuristic decision-making. Essential for predicting deviations from neoclassical utility maximization in consumer and financial markets.

## Technical Deep-Dive

Implements Prospect Theory value functions, hyperbolic discounting for time inconsistency, and probability weighting functions. Uses reinforcement learning to simulate habit formation and availability cascades.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| choices | List[Dict] | Available choice set |
| frame | str | Choice architecture framing |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| predicted_choice | str | Choice selected by bounded agent |
| bias_flag | str | Dominant cognitive bias active |

### State Schema
- `bias_profile`: Latent bias parameters (loss aversion, beta-delta).

## Dependencies
- Upstream: None
- Downstream: H11-MICROECON, H11-MARKETING

> **Layer 22** · Humanities & Social Sciences · `H11-NEUROSCIENTIA`

## Purpose

H11-NEUROSCIENTIA provides a low-level biological grounding for the cognitive processes in the Humanities & Social substrate. It models neuromodulation (Dopamine, Serotonin, Cortisol), synaptic plasticity, and bio-energetic constraints.

## Technical Deep-Dive

The agent implements a Leaky Integrate-and-Fire (LIF) abstracted network coupled with a Global Neuromodulator Field (GNF). Instead of tracking billions of synapses, it tracks macro-region states (e.g., Amygdala hyper-activation, Prefrontal Cortex inhibition).

Hebbian learning (Spike-Timing-Dependent Plasticity - STDP) is approximated via continuous state vectors. Cortisol accumulation acts as a dampening multiplier on synaptic weights, simulating stress-induced cognitive impairment.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| systemic_stress | float | Environmental stress load |
| reward_signal | float | Exogenous reinforcement |
| active_regions | List[str] | Brain areas engaged by task |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| neuromodulator_levels | Dict[str, float] | Levels of DA, 5-HT, CORT |
| synaptic_plasticity | float | Global rate of learning |
| energetic_drain | float | Metabolic cost |

### State Schema
Maintains `BioState`, tracking the homeostasis and depletion of neuro-chemical reservoirs.

## Dependencies

### Upstream (depends on)
(Root-level physics engine inputs)

### Downstream (feeds into)
H11-COGNITIVA, H11-PSYCHOLOGIA

## Failure Modes
1. Excitotoxicity (over-activation causes cell death/node deletion).
2. Cortisol Lock (chronic stress permanently drops plasticity to 0).

## Performance Characteristics
Low latency required to supply neuromodulation bounds to higher cognitive models.

## Research References
- Dayan, P., & Abbott, L. F. (2001). Theoretical Neuroscience.
- Friston, K. (2010). The free-energy principle: a unified brain theory?

## Implementation Notes
Use exponential decay functions for neuromodulator clearance to maintain homeostatic baselines.

> **Layer 22** · Humanities & Social Sciences · `H11-POLITICALSCI`

## Purpose

H11-POLITICALSCI analyzes and simulates power dynamics, governance structures, and institutional behavior. It models how power is distributed, how institutions constrain behavior, and how systemic political shifts (e.g., democratization, autocratization) occur across large populations of simulated actors.

## Technical Deep-Dive

The agent implements an Institutional Power Network (IPN) model, heavily influenced by Selectorate Theory (Bueno de Mesquita et al.). It models the interplay between the Nominal Selectorate, Real Selectorate, and Winning Coalition.

Graph centrality metrics (Eigenvector, Betweenness) within the IPN determine the political capital of nodes. Institutional stability is calculated dynamically by solving differential equations representing resource extraction vs. public goods provisioning.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| population_graph | Dict[str, Any] | Network of political actors |
| resource_allocation | Dict[str, float] | Flow of political capital/money |
| institutional_rules | Dict[str, Any] | Current regime parameters |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| stability_index | float | Likelihood of regime survival |
| power_distribution | Dict[str, float] | Centrality/power of key actors |
| predicted_shifts | List[str] | Forecasted regime changes (e.g. coup) |

### State Schema
Maintains `RegimeState`, encapsulating the current size of the winning coalition and historical taxation rates.

## Dependencies

### Upstream (depends on)
H11-ETHICA-APPLIED, H11-PSYCHOLOGIA

### Downstream (feeds into)
H11-INTERNATIONAL, H11-PUBLICPOLICY

## Failure Modes
1. Coalition Fragmentation (the winning coalition drops below critical mass, throwing the simulation into infinite loop anarchy).
2. Capital Overflow (a single node acquires 100% of resources, breaking continuous equations).

## Performance Characteristics
High memory for storing large population graphs; requires optimized sparse matrix solvers for centrality calculations.

## Research References
- Bueno de Mesquita, B. et al. (2003). The Logic of Political Survival.
- Acemoglu, D., & Robinson, J. A. (2005). Economic Origins of Dictatorship and Democracy.

## Implementation Notes
Eigenvector centrality must use power iteration methods with a strict tolerance to handle massive, rapidly updating population graphs.

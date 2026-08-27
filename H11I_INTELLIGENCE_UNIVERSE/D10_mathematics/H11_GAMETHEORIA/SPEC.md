> **Layer 10** · Mathematics · `H11-GAMETHEORIA`

## Purpose

The H11-GAMETHEORIA agent models strategic interactions among rational decision-makers. It computes equilibria for both cooperative and non-cooperative games. In the H11 substrate, it provides the mathematical foundation for multi-agent reinforcement learning, economics simulations, and protocol mechanism design (e.g., auction theory).

## Technical Deep-Dive

H11-GAMETHEORIA uses the Lemke-Howson algorithm for finding Nash Equilibria in bimatrix games. For extensive-form games, it applies Backward Induction and Subgame Perfect Equilibrium (SPE) logic. It also supports incomplete information via Bayesian Nash Equilibria.

In cooperative settings, it calculates Shapley values and the Core to determine fair payoff distributions among coalitions. Mechanism design capabilities include verifying strategy-proofness and incentive compatibility for VCG (Vickrey-Clarke-Groves) auctions.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `payoff_matrices` | `List[List[float]]` | Payoffs for N players |
| `game_tree` | `Dict` | Nodes, information sets |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `nash_equilibria` | `List[Dict]` | Strategies |
| `shapley_values` | `Dict[str, float]` | Payouts |

### State Schema
`solved_subgames`: Memoization for extensive-form games to prune branches during backward induction.

## Dependencies

### Upstream (depends on)
- `H11-OPTIMIZATIO`: For solving linear complementarity problems (LCP).
- `H11-PROBABILITAS`: For expected utility over belief spaces.

### Downstream (feeds into)
- Higher-level economic or sociocognitive agents.

## Failure Modes
- Infinite loops in fictitious play when cyclic equilibria exist (e.g., Rock-Paper-Scissors with perturbed payouts).
- Intractability of Shapley value computation due to $2^N$ coalition space.

## Performance Characteristics
Finding Nash Equilibria is PPAD-complete; thus, runtime can scale exponentially in worst-case bimatrix games.

## Research References
- Nash, J. (1951). Non-Cooperative Games.
- Shapley, L. S. (1953). A Value for n-Person Games.

## Implementation Notes
Payoff matrices should be passed as sparse tensors if action spaces are large but mostly yield zero payoffs. Approximation algorithms are required for computing Shapley values when $N > 20$.

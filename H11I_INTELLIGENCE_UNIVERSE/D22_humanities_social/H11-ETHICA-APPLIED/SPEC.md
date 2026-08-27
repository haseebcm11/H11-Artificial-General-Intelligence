> **Layer 22** · Humanities & Social Sciences · `H11-ETHICA-APPLIED`

## Purpose

H11-ETHICA-APPLIED acts as a normative rule-engine and moral decision simulator. Using values assigned by H11-AXIOLOGIA, it evaluates proposed actions within a socio-cultural matrix to determine their ethical validity based on multiple normative frameworks (Deontology, Consequentialism, Virtue Ethics).

## Technical Deep-Dive

The agent uses a Multi-Framework Moral Solver (MFMS). It encodes ethical frameworks as constraint satisfaction problems (CSPs) and utility optimization models. 
- **Deontology** is modeled via strictly evaluated propositional logic bounds.
- **Consequentialism** is modeled via utilitarian reward function gradients over future time steps.
- **Virtue Ethics** is evaluated via character-trajectory similarity matching using embedding spaces.

The solver computes a weighted Pareto frontier across these three axes to propose the most "ethically robust" action.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| action_proposal | Dict[str, Any] | The action to be evaluated |
| context_state | Dict[str, Any] | The current environmental state |
| actor_profile | Dict[str, Any] | Historical profile of the actor |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ethical_verdict | bool | Is the action approved? |
| framework_scores | Dict[str, float] | Scores across deont/conseq/virtue |
| required_modifications | List[str] | Suggestions to improve ethicality |

### State Schema
Maintains `NormativeConstraints`, which dynamically updates based on societal drift from H11-CULTURAL.

## Dependencies

### Upstream (depends on)
H11-AXIOLOGIA, H11-PUBLICPOLICY

### Downstream (feeds into)
H11-POLITICALSCI

## Failure Modes
1. Ethical Gridlock (no action satisfies the Pareto frontier).
2. Consequential explosion (utility gradients diverge to infinity due to butterfly effects).

## Performance Characteristics
High latency due to simulation roll-outs for consequentialist evaluation.

## Research References
- Kant, I. (1785). Groundwork of the Metaphysics of Morals.
- Mill, J. S. (1861). Utilitarianism.
- Foot, P. (1967). The Problem of Abortion and the Doctrine of the Double Effect (Trolley Problem).

## Implementation Notes
Use Monte Carlo Tree Search (MCTS) for the consequentialist branch to bound the rollout explosion.

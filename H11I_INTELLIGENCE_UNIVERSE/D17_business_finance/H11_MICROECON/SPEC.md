> **Layer 17** · Business, Finance & Economics · `H11-MICROECON`

## Purpose

The H11-MICROECON agent is responsible for modeling individual and firm-level decision-making. It analyzes supply and demand dynamics, pricing strategies, market structures, and consumer utility optimization.

## Technical Deep-Dive

This agent employs advanced microeconomic modeling techniques, including Walrasian equilibrium solvers, Cournot and Bertrand competition models, and discrete choice models for consumer behavior. It utilizes constrained optimization to simulate profit maximization and utility maximization under budget constraints.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| market_structure | MarketType | Monopoly, Oligopoly, Perfect Competition |
| demand_function | Callable | Price to Quantity mapping |
| cost_function | Callable | Quantity to Cost mapping |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| optimal_price | float | Profit-maximizing price |
| optimal_quantity | float | Profit-maximizing quantity |
| deadweight_loss | float | Efficiency loss |

### State Schema
- `market_history`: List of past market equilibria.
- `elasticity_estimates`: Price and income elasticities.

## Dependencies

### Upstream (depends on)
- H11-BEHAVIORALECON

### Downstream (feeds into)
- H11-MACROECON
- H11-FINANCIA

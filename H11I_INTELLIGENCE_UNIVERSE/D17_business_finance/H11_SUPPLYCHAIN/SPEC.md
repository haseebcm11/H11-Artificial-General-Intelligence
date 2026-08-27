> **Layer 17** · Business, Finance & Economics · `H11-SUPPLYCHAIN`

## Purpose
Models logistics, inventory routing, bullwhip effect mitigation, and network design.

## Technical Deep-Dive
Implements the Newsvendor model for perishable inventory and mixed-integer linear programming (MILP) heuristics for the facility location problem.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| demand_mean | float | Expected demand |
| demand_std | float | Demand volatility |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| order_qty | float | Optimal order |

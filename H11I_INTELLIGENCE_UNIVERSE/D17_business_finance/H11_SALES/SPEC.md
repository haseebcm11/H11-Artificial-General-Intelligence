> **Layer 17** · Business, Finance & Economics · `H11-SALES`

## Purpose
Models sales funnels, conversion rates, pipeline velocity, and territory optimization.

## Technical Deep-Dive
Implements Markov chain models for sales stage transitions. Uses linear programming for sales quota allocation and territory balancing.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| leads | int | Number of prospects |
| conversion_rates | List[float] | Rates between stages |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| closed_won | int | Deals closed |

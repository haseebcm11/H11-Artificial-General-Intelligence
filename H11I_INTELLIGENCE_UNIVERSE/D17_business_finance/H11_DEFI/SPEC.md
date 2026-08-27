> **Layer 17** · Business, Finance & Economics · `H11-DEFI`

## Purpose
Models automated market makers (AMMs), liquidity pools, and flash loans.

## Technical Deep-Dive
Implements constant product formulas (x*y=k) for decentralized exchanges. Calculates impermanent loss and yield farming APYs.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| pool_x | float | Token X liquidity |
| pool_y | float | Token Y liquidity |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| exchange_rate | float | Implied rate |

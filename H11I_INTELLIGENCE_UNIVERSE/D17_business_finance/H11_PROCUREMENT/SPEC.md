> **Layer 17** · Business, Finance & Economics · `H11-PROCUREMENT`

## Purpose
Models strategic sourcing, vendor negotiations, and purchasing optimization.

## Technical Deep-Dive
Implements auction theory (Vickrey auctions, first-price sealed-bid) for supplier selection. Uses economic order quantity (EOQ) and total cost of ownership (TCO) models.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| demand_rate | float | Annual demand |
| order_cost | float | Cost per order |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| eoq | float | Optimal order qty |

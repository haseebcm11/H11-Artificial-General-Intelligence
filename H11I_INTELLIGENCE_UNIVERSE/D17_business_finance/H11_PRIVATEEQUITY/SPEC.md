> **Layer 17** · Business, Finance & Economics · `H11-PRIVATEEQUITY`

## Purpose
Models leveraged buyouts (LBO), fund structures (GP/LP), and operational value creation.

## Technical Deep-Dive
Implements debt schedules with senior/mezzanine tranches, cash sweep mechanics, and waterfall distribution models (European vs American hurdles).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ebitda | float | Target EBITDA |
| entry_multiple | float | Entry valuation |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| moic | float | Multiple on Invested Capital |

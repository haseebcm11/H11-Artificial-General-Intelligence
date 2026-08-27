> **Layer 17** · Business, Finance & Economics · `H11-MA`

## Purpose
Analyzes M&A transactions, synergies, accretion/dilution, and antitrust implications.

## Technical Deep-Dive
Implements pro-forma EPS calculations to determine if a deal is accretive or dilutive. Models control premiums, exchange ratios in stock deals, and integration costs.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| acquirer_eps | float | EPS of buyer |
| target_eps | float | EPS of target |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| accretion | float | Change in EPS |

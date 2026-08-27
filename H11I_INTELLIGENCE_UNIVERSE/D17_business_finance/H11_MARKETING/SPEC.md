> **Layer 17** · Business, Finance & Economics · `H11-MARKETING`

## Purpose
Models marketing mix modeling (MMM), customer acquisition cost (CAC), and brand equity.

## Technical Deep-Dive
Implements advertising Adstock transformations, diminishing returns (S-curves), and multi-touch attribution (Shapley value).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ad_spend | Dict | Spend by channel |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| acquisitions | int | New customers |

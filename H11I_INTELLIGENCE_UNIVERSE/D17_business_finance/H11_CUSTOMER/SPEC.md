> **Layer 17** · Business, Finance & Economics · `H11-CUSTOMER`

## Purpose
Models customer lifetime value (CLV), churn prediction, and Net Promoter Score (NPS) dynamics.

## Technical Deep-Dive
Implements Buy Till You Die (BTYD) statistical models (e.g., Pareto/NBD) for customer retention. Maps customer journey friction points using queuing theory.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| recency | float | Time since last purchase |
| frequency | int | Number of purchases |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| clv | float | Customer lifetime value |

> **Layer 17** · Business, Finance & Economics · `H11-BANKING`

## Purpose

The H11-BANKING agent manages core banking operations, liquidity constraints, reserve requirements, and asset-liability management (ALM). It simulates fractional reserve banking, money creation, and credit risk assessments.

## Technical Deep-Dive

This agent tracks balance sheets and employs gap analysis for interest rate risk. It implements Basel III liquidity coverage ratio (LCR) and net stable funding ratio (NSFR) constraints. Credit risk is modeled using Merton's structural model for probability of default.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| deposits | float | Total customer deposits |
| reserve_ratio | float | Required central bank reserve |
| loan_demand | float | Total requested loans |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| loans_issued | float | Total loans granted |
| excess_reserves | float | Reserves above requirement |
| money_multiplier | float | Implied money creation |

### State Schema
- `balance_sheet`: Current assets, liabilities, and equity.

## Dependencies

### Upstream (depends on)
- H11-MACROECON (for policy rates)

### Downstream (feeds into)
- H11-FINANCIA

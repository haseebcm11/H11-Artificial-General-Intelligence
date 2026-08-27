> **Layer 17** · Business, Finance & Economics · `H11-FINANCIA`

## Purpose

The H11-FINANCIA agent handles corporate finance operations, capital structure optimization, dividend policy, and valuation modeling. It evaluates project NPV, IRR, and determines the optimal Weighted Average Cost of Capital (WACC).

## Technical Deep-Dive

This agent uses advanced Discounted Cash Flow (DCF) models, the Capital Asset Pricing Model (CAPM) for cost of equity, and Monte Carlo simulations for cash flow risk. It models debt schedules and tax shields to find the optimal debt-to-equity ratio that minimizes WACC.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| cash_flows | List[float] | Projected cash flows |
| risk_free_rate | float | Market risk-free rate |
| market_risk_premium | float | Market premium |
| beta | float | Asset beta |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| enterprise_value | float | Calculated firm EV |
| equity_value | float | Calculated firm equity |
| wacc | float | Firm discount rate |
| irr | float | Internal rate of return |

### State Schema
- `valuation_history`: Past valuations and assumptions.

## Dependencies

### Upstream (depends on)
- H11-MACROECON (for rates)

### Downstream (feeds into)
- H11-MA
- H11-PRIVATEEQUITY

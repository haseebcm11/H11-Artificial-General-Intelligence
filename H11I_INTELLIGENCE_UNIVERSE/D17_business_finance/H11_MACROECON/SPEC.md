> **Layer 17** · Business, Finance & Economics · `H11-MACROECON`

## Purpose

The H11-MACROECON agent models aggregate economic phenomena, including GDP growth, inflation, unemployment, and monetary/fiscal policy impacts. It provides macroeconomic forecasting and systemic risk analysis.

## Technical Deep-Dive

This agent utilizes Dynamic Stochastic General Equilibrium (DSGE) models, Vector Autoregression (VAR), and Phillips Curve estimations. It simulates central bank policy responses using Taylor Rules and analyzes fiscal multipliers for government spending and taxation.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| gdp_current | float | Current GDP |
| inflation_rate | float | Current inflation |
| policy_rate | float | Central bank interest rate |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| forecasted_gdp | float | Next period GDP |
| forecasted_inflation | float | Next period inflation |
| policy_recommendation | float | Recommended interest rate |

### State Schema
- `time_series_data`: Historical macroeconomic indicators.
- `shock_history`: Exogenous shocks applied.

## Dependencies

### Upstream (depends on)
- H11-MICROECON

### Downstream (feeds into)
- H11-TRADE
- H11-BANKING

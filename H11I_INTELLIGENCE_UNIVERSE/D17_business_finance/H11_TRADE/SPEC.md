> **Layer 17** · Business, Finance & Economics · `H11-TRADE`

## Purpose
Models international trade flows, comparative advantage, tariffs, and exchange rate dynamics.

## Technical Deep-Dive
Implements Ricardian and Heckscher-Ohlin models, gravity models of trade, and iceberg transport costs.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| home_endowments | Dict | Home country factors |
| foreign_endowments | Dict | Foreign country factors |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| trade_volume | float | Volume of trade |
| exchange_rate | float | FX rate |

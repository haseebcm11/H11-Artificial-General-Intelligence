> **Layer 19** · Arts, Design & Creativity · `H11-CERAMICA`

## Purpose
Simulates wheel-throwing, hand-building, and the chemical transformation of clay and glaze during kiln firing.

## Technical Deep-Dive
Models thermal expansion coefficients (COE) to predict glaze crazing or shivering based on the Seger formula for ceramic chemistry.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| profile_curve | List | Spin profile |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| shrinkage_factor | float | Post-firing scale |

### State Schema
- `is_firing`: Boolean.

## Dependencies
- Upstream: None

## Failure Modes
- Thermal shock shattering.

## Performance Characteristics
Low compute.

## Implementation Notes
Implement revolution solids for wheel throwing.

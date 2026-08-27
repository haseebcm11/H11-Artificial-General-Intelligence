> **Layer 19** · Arts, Design & Creativity · `H11-ILLUSTRATIO`

## Purpose
Generates resolution-independent vector graphics using generative spline math.

## Technical Deep-Dive
Applies Ramer-Douglas-Peucker algorithm to simplify complex generated paths into clean Bezier curves.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| prompt_concept | str | Intent |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| svg_data | bytes | XML payload |

### State Schema
- `paths_drawn`: Int.

## Dependencies
- Downstream: Web rendering

## Failure Modes
- Self-intersecting polygons breaking fill rules.

## Implementation Notes
Use non-zero winding rules for boolean path operations.

> **Layer 19** · Arts, Design & Creativity · `H11-WOODWORK`

## Purpose
Generates optimized cut lists, calculates grain expansion, and designs dovetail/mortise-and-tenon joints.

## Technical Deep-Dive
Employs 2D bin packing algorithms (Guillotine cut) to minimize board waste when generating the cut list.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| furniture_spec | Dict | Dimensions |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| cut_list | List | Optimized cuts |

### State Schema
- `joints_calculated`: Int.

## Dependencies
- Downstream: CNC Machine

## Failure Modes
- Cross-grain gluing failure.

## Implementation Notes
Include kerf thickness in bin packing constraints.

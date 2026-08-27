> **Layer 19** · Arts, Design & Creativity · `H11-CALLIGRAPHIA`

## Purpose
Simulates broad-edge and pointed-pen nib dynamics to generate organic typography.

## Technical Deep-Dive
Models ink flow and nib spread using variable-width stroke algorithms dependent on simulated pressure and velocity.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| text | str | String |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| stroke_vectors | bytes | Vector paths |

### State Schema
- `words_written`: Int.

## Dependencies
- Downstream: Graphic Design

## Failure Modes
- Improper ligature joins.

## Implementation Notes
Use quaternion rotation for nib angle tracking during curves.

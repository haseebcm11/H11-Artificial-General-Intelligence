> **Layer 19** · Arts, Design & Creativity · `H11-ORIGAMI`

## Purpose
Solves origami mathematics to translate 3D shapes into 2D flat-foldable crease patterns.

## Technical Deep-Dive
Implements Robert Lang's TreeMaker algorithm. Applies Kawasaki's and Maekawa's theorems to ensure theoretical flat-foldability of vertex nodes.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| target_3d_mesh | bytes | 3D target |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| crease_pattern_svg | bytes | 2D vector |

### State Schema
- `folds_calculated`: Int.

## Dependencies
- Upstream: 3D Modeler

## Failure Modes
- NP-Hard tree generation timeout.

## Implementation Notes
Use high precision floats for vertex calculations.

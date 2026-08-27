> **Layer 19** · Arts, Design & Creativity · `H11-DIGITALART`

## Purpose
Merges multi-pass 3D renders, matte paintings, and photography into cohesive visuals.

## Technical Deep-Dive
Implements a DAG (Directed Acyclic Graph) engine for evaluating pixel operations in floating-point linear color space.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| matte_masks | List | Alpha masks |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| composited_image | bytes | EXR output |

### State Schema
- `nodes_evaluated`: Int.

## Dependencies
- Upstream: 3D Render
- Downstream: Publisher

## Failure Modes
- Pre-multiplied alpha channel artifacts.

## Implementation Notes
Ensure strict ACES color management.

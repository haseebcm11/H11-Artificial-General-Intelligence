# H11-OBJECT-PERMANENCE — Object Permanence

> **Layer 12** · World Models & Simulation · `H11-OBJECT-PERMANENCE`

## Purpose
Tracks named objects across frames, marking them occluded when missing rather than deleting them.

## Technical Deep-Dive
Each observation is {id, x, y, visible}. If visible is false or the id is absent this frame, the last pose is retained with occluded=True. Identity switches are a documented failure when ids are not supplied.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| frame | `List[dict]` | Detections this frame |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| slots | `List[dict]` | Tracked objects including occluded |

### State Schema
tracked: Dict[str, dict]

## Dependencies
### Upstream (depends on)
`H11-WORLDMODEL`

### Downstream (feeds into)
`H11-AGENT-MODEL`

## Failure Modes
- Detections without id are dropped.
- Two detections sharing an id: last write wins.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Baillargeon (1987). Object permanence in 3.5- and 4.5-month-old infants.
- Locatello et al. (2020). Object-Centric Learning with Slot Attention.

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.

# H11-VECTORDb — Vector Database

> **Layer 3** · Representation & Embedding · `H11-VECTORDb`

## Purpose
In-memory store of named vectors with insert, get, delete, and listing.

## Technical Deep-Dive
Records are keyed by string id. No disk layout; this agent is the CRUD contract that H11-INDEX and H11-SIMILARITY read from.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| op | `str` | PUT|GET|DELETE|LIST |
| record_id | `str` | Key |
| vector | `List[float]` | Payload for PUT |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| ok | `bool` | Whether the op succeeded |
| record | `Optional[dict]` | Fetched record |
| ids | `List[str]` | LIST result |

### State Schema
store: Dict[str, List[float]]

## Dependencies
### Upstream (depends on)
`H11-EMBEDDER`

### Downstream (feeds into)
`H11-INDEX`, `H11-SIMILARITY`

## Failure Modes
- GET/DELETE of a missing id returns ok=false rather than raising.
- PUT with empty id is rejected.

## Performance Characteristics
Stdlib reference implementation. Suitable as an enabling embodiment and
contract test, not as a production kernel.

## Research References
- Johnson, Douze, Jégou (2017). Billion-scale similarity search with GPUs (contract-level).

## Implementation Notes
No third-party ML frameworks. Deterministic where possible so composition tests can assert outputs.

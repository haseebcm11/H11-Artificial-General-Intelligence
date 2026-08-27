# H11-DERMATOLOGIA — Dermatologia

> **Layer I** · Intelligence Universe · `H11-DERMATOLOGIA`

## Purpose
# H11-DERMATOLOGIA SPEC\n 

## Technical Deep-Dive
Stdlib reference kernel unique to `H11-DERMATOLOGIA`. Deterministic, no third-party ML, no generator template.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| payload | object | Domain fields for this specialist |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| agent_id | string | Echo of `H11-DERMATOLOGIA` |
| (kernel fields) | any | Specialist-specific measurements |

## Failure Modes
- Missing required domain fields raise `DERMATOLOGIAError`.

## Implementation Notes
No asyncio.sleep stubs. Process is a real function of the payload.

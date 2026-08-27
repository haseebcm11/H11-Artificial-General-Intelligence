> **Layer 21** · Literature & Linguistics · `H11-DRAMA`

## Purpose
The H11-DRAMA agent models theatrical dialogue, character interactions, and structural flow of plays. It abstracts dramatic elements into tension-arcs, dialogue-turns, and subtext modeling. It generates scripts that balance character voices, maintain realistic conversational dynamics, and follow dramatic structures (e.g., three-act or five-act).

## Technical Deep-Dive
DRAMA employs multi-agent dialogue simulation where each character is modeled as a partially-observable Markov decision process (POMDP), tracking beliefs about other characters. This enables subtextual generation—where characters say one thing but mean another.
The tension arc is parameterized via a differential equation that dictates the target sentiment/conflict level for a given scene, guiding the generation process to escalate or de-escalate dialogue intensity accordingly.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| characters | List[Dict] | Character profiles with goals and traits |
| conflict_type | str | Primary conflict driving the scene |
| act_structure | str | Requested structure (e.g., "three-act") |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| script | str | The generated theatrical script |
| tension_metrics | List[float] | Calculated tension level per scene |

### State Schema
Tracks the current scene, active characters, their relationship matrix, and global tension accumulator.

## Dependencies
- H11-NARRATIO (for overarching plot)
- H11-PRAGMATICA (for speech acts and dialogue intent)

## Failure Modes
- `TensionStagnation`: The scene fails to build adequate conflict or resolution.
- `VoiceConvergence`: Characters begin sounding identical due to homogenization in the generation distribution.

## Performance Characteristics
Heavy memory usage per character context. State updates after every dialogue turn.

## Research References
- "Computational Modeling of Dramatic Tension"
- "POMDPs for Subtext in Dialogue Generation"

## Implementation Notes
Use character-specific LoRA adapters if fine-tuning generation models for distinct voices.

> **Layer 10** · Memory Architecture · `H11-CONSOLIDATE`

## Purpose
The H11-CONSOLIDATE agent manages the critical biological analogue of sleep/offline-replay. It transfers volatile, short-term episodic experiences into stable, long-term semantic structures. It utilizes spaced repetition algorithms to ensure synaptic consolidation of high-value information while pruning noisy or irrelevant data.

## Technical Deep-Dive
Consolidation happens via Prioritized Experience Replay (PER). Memories are scored based on Surprise (TD-error in reinforcement learning contexts) and Emotional Salience. High-scoring memories are re-activated (replayed) against the model offline to induce weight updates (or vector indexing into long-term DBs).
The agent integrates SuperMemo-2 style spaced repetition math to schedule when a memory trace needs to be reactivated to prevent the Ebbinghaus forgetting curve from crossing a minimum retention threshold.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `buffer_items` | `List[MemoryTrace]` | Recent episodic events. |
| `salience_threshold` | `float` | Minimum importance to keep. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `consolidated_items` | `List[MemoryTrace]` | Items moved to long term. |
| `pruned_items` | `List[str]` | IDs of forgotten/dropped items. |

### State Schema
Maintains a `ReplayBuffer` and an `IntervalSchedule` for mapping when items next need structural reinforcement.

## Dependencies
### Upstream
- `H11-WORKING`: The transient short-term buffer.
- `H11-EPISODIC`: Source of recent day-to-day events.
### Downstream
- `H11-SEMANTIC`: Long-term stable storage receiving the abstractions.

## Failure Modes
- **Catastrophic Interference**: New memories overwrite overlapping old memories if replay isn't balanced.
- **Replay Bottleneck**: Too much data, not enough offline cycles (sleep deprivation equivalent).
- **Over-fitting**: Replaying the same outlier memory too often, causing hallucinated importance.

## Performance Characteristics
- Batch processing: Runs primarily in idle/background states.
- I/O bound: Heavy writes to vector databases and graph schemas.

## Research References
- McClelland, J. L., et al. (1995). Why there are complementary learning systems in the hippocampus and neocortex.
- Wozniak, P. (1990). Optimization of learning (SuperMemo algorithms).

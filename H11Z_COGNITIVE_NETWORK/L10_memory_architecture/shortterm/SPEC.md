> **Layer 10** · Memory Architecture · `H11-SHORTTERM`

## Purpose
The H11-SHORTTERM agent acts as a transient, sliding-window storage system that bridges the gap between the highly constrained active processing buffer (H11-WORKING) and permanent semantic/episodic storage. It is responsible for maintaining information over periods of seconds to minutes. It fundamentally relies on trace decay algorithms and rehearsal mechanisms to implement classical psychological phenomena such as primacy and recency effects.

## Technical Deep-Dive
H11-SHORTTERM utilizes a temporal graph structure where nodes represent concepts and edges represent sequential adjacency. Memory persistence is modeled via a power-law forgetting curve (Ebbinghaus decay), parameterized dynamically based on item complexity and affective valence.

To model serial position effects (primacy and recency), the storage mechanism assigns a heightened initial strength to the first few items in a sequence (primacy via reduced proactive interference) and relies on the lack of retroactive interference to preserve the latest items (recency). A sliding window garbage collector periodically sweeps the graph, pruning nodes that fall below a critical activation threshold.

Items that are repeatedly accessed or actively transferred back to H11-WORKING receive structural reinforcement, simulating Long-Term Potentiation (LTP) early stages, which flags them as candidates for consolidation by H11-LONGTERM.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `sequence_id` | `UUID` | Associates items with a continuous experiential sequence. |
| `items` | `List[Dict]` | Set of items evicted from H11-WORKING or freshly arriving. |
| `affect_valence` | `float` | Emotional/importance weighting [-1.0 to 1.0]. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `consolidable_traces` | `List[Trace]` | Items exceeding threshold, ready for Long-Term storage. |
| `retrieved_items` | `List[Dict]` | Results of queries to short-term memory. |
| `decay_events` | `int` | Number of items permanently forgotten this cycle. |

### State Schema
Maintains a Time-Annotated Sequential Graph. Nodes track activation energy, creation timestamp, and access history. 

## Dependencies
### Upstream (depends on)
- `H11-WORKING`: Receives evicted high-salience items.
### Downstream (feeds into)
- `H11-LONGTERM`: Provides consolidated traces.
- `H11-EPISODIC`: Provides sequential binding context.

## Failure Modes
- **Catastrophic Interference**: Rapid influx of highly similar items overwriting existing traces due to trace blending.
- **Collector Thrashing**: The garbage collector consuming excessive compute when threshold variance is high.
- **Context Loss**: Sequence IDs breaking, leading to isolated items that cannot leverage associative recall.

## Performance Characteristics
Designed for medium latency (~20ms) and moderate throughput. Memory capacity is soft-bounded, typically holding hundreds of items, scaling linearly with the retention window (e.g., 5 minutes).

## Research References
- Ebbinghaus, H. (1885). Memory: A contribution to experimental psychology.
- Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes.
- Brown, G. D., Preece, T., & Hulme, C. (2000). Oscillator-based memory for serial order.

## Implementation Notes
Implement the Ebbinghaus decay strictly as `R = e^(-t/S)` where `S` is the relative strength of memory. Ensure the garbage collector runs asynchronously to prevent blocking the read/write paths.

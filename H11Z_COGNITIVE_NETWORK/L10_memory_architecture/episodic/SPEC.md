> **Layer 10** · Memory Architecture · `H11-EPISODIC`

## Purpose
The H11-EPISODIC agent acts as the autobiographical ledger of the cognitive substrate. Unlike Semantic memory, which stores detached facts, Episodic memory binds information to a specific temporal, spatial, and agentic context. It allows the system to engage in "mental time travel," replaying past experiences to extract new insights or inform future planning via experience replay.

## Technical Deep-Dive
Episodic memory requires continuous contextual binding. H11-EPISODIC implements this via a Recurrent Spatiotemporal Binding (RSB) algorithm. Each encoded episode is not just a snapshot, but a compressed trajectory of states. 

The agent utilizes a hierarchical segmentation model to break a continuous stream of experiences into discrete "episodes" based on prediction error spikes (event boundaries). When the prediction error of the current sensory stream exceeds a threshold, an event boundary is formed, and the previous sequence is packaged, summarized, and stored.

Retrieval relies on Pattern Completion. A partial cue (e.g., a specific entity or a timestamp) triggers the reconstruction of the entire episode. The agent also supports an `experience_replay` mode, where it iterates over chronologically adjacent episodes, feeding them to H11-WORKING to simulate dreaming or off-line reinforcement learning.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `state_snapshot` | `Dict` | A frame of the system's current holistic state. |
| `prediction_error` | `float` | Metric from the predictive coding layers. |
| `context_metadata` | `ContextMap` | Spatial, temporal, and emotional coordinates. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `episode_summary` | `String` | Abstracted textual summary of a completed episode. |
| `replayed_states` | `List[Dict]` | Trajectory of states generated during replay. |
| `boundary_detected` | `bool` | True if the input triggered a new episode segment. |

### State Schema
An ordered chronological log of Episodes, each containing a sequence of StateFrames and a ContextMap. Contains pointers to H11-LONGTERM for large payload storage.

## Dependencies
### Upstream (depends on)
- `H11-SHORTTERM`: Derives sequences and transient associations.
- `H11-PREDICTION`: Uses prediction error to determine event boundaries.
### Downstream (feeds into)
- `H11-WORKING`: Feeds reconstructed experiences during replay.
- `H11-SEMANTIC`: Provides raw experiential data for semantic abstraction over time.

## Failure Modes
- **Boundary Failure**: Failure to segment continuous time, leading to massive, un-retrievable "mega-episodes".
- **Confabulation**: Pattern completion hallucinating details that were never present in the original episode.
- **Context Bleed**: Emotional or spatial metadata improperly linking completely unrelated episodes together.

## Performance Characteristics
Encoding is a fast append operation, but episode summarization and pattern completion are computationally expensive. Throughput is bounded by the frequency of event boundaries (typically 1-5 per minute of active processing).

## Research References
- Tulving, E. (2002). Episodic memory: From mind to brain.
- Zacks, J. M., Speer, N. K., Swallow, K. M., Braver, T. S., & Reynolds, J. R. (2007). Event perception: a mind-brain perspective.
- Hassabis, D., Kumaran, D., Vann, S. D., & Maguire, E. A. (2007). Patients with hippocampal amnesia cannot imagine new experiences.

## Implementation Notes
Pay special attention to the event segmentation threshold. If it's too sensitive, the system will generate too many disjointed micro-episodes. Use an exponentially weighted moving average (EWMA) of prediction errors to dynamically adjust the threshold.

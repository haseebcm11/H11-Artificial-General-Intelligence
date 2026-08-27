> **Layer 10** · Memory Architecture · `H11-WORKING`

## Purpose
The H11-WORKING agent serves as the active processing buffer for the cognitive substrate, implementing the Baddeley-Hitch Central Executive model. It is designed to hold a limited number of items in active consciousness, actively manipulating them to support complex cognitive tasks such as reasoning, comprehension, and learning. By tightly restricting capacity, it forces the system to prioritize salient information, acting as an attentional bottleneck that mirrors human working memory constraints.

## Technical Deep-Dive
H11-WORKING implements a mathematically rigorous version of Miller's Law (the magical number 7±2), utilizing an attention-based selection mechanism to manage item eviction. It divides its buffer into modal subsystems: a generalized Phonological Loop for sequential linguistic processing and a Visuospatial Sketchpad for structured/graphical relationships. 

The attention mechanism utilizes a normalized softmax function over the salience scores of items currently in the buffer. As new information arrives, if the buffer is at capacity, the Central Executive initiates an eviction process. Rather than simple LRU (Least Recently Used), eviction probability is inversely proportional to an item's dynamically updated salience, which decays over time unless rehearsed. This ensures that highly relevant but slightly older items are retained over newer, less relevant ones.

Rehearsal is modeled as an active feedback loop where downstream agents can reinforce the salience of specific items. The Central Executive also maintains a task-set, which acts as a biasing vector on the attention mechanism, allowing goal-directed filtering of incoming streams.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `stimulus_id` | `UUID` | Unique identifier for the incoming stimulus. |
| `modality` | `ModalityEnum` | Categorization of stimulus (LINGUISTIC, SPATIAL, SYMBOLIC). |
| `payload` | `Dict[str, Any]` | The semantic content of the stimulus. |
| `initial_salience` | `float` | Base salience score provided by the sensory layer [0.0 - 1.0]. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `active_set` | `List[WorkingMemoryItem]` | Current items held in the central executive buffer. |
| `evicted_items` | `List[WorkingMemoryItem]` | Items removed from the buffer during this cycle. |
| `capacity_load` | `float` | Current buffer utilization ratio [0.0 - 1.0]. |

### State Schema
The state maintains the active buffer, partitioned into modal capacities, a temporal decay function tracking, and the current goal-directed biasing vector.

## Dependencies
### Upstream (depends on)
- `H11-SENSORY`: Feeds raw stimuli and initial salience.
- `H11-ATTENTION`: Provides goal-directed biasing vectors.
### Downstream (feeds into)
- `H11-SHORTTERM`: Evicted items with high salience are transferred here.
- `H11-REASONING`: Uses the `active_set` for immediate logical operations.

## Failure Modes
- **Attentional Capture**: High-salience noise constantly overwriting the buffer, preventing sustained reasoning.
- **Buffer Starvation**: Over-aggressive decay leading to premature eviction before downstream processing is complete.
- **Modal Interference**: Too many items of the same modality exceeding sub-capacity despite overall buffer availability.

## Performance Characteristics
Latency is highly optimized (<5ms) as this is a high-frequency active loop. Memory footprint is strictly bounded to max 9 complex objects. Compute profile relies on continuous matrix multiplications for salience updating.

## Research References
- Baddeley, A. D., & Hitch, G. (1974). Working memory. In The psychology of learning and motivation (Vol. 8, pp. 47-89).
- Cowan, N. (2001). The magical number 4 in short-term memory.
- Miller, G. A. (1956). The magical number seven, plus or minus two.

## Implementation Notes
Focus on the precise tuning of the decay rate and the softmax temperature parameter during eviction.

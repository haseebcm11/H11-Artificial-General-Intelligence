> **Layer 10** · Memory Architecture · `H11-TEMPORAL-MEM`

## Purpose
The H11-TEMPORAL-MEM agent grounds the cognitive substrate in time. While semantic memory is static and episodic memory is sequential, temporal memory provides non-linear time-awareness. It calculates retention probabilities based on human-like forgetting curves (Ebbinghaus) and manages the chronological interleaving of events.

This agent is crucial for answering queries like "What happened right before the system crashed last Tuesday?" or "Summarize how my coding style evolved over the last six months." It prevents the AI from treating all retrieved memories as occurring simultaneously, preserving the arrow of time in context windows.

## Technical Deep-Dive
The agent employs a Continuous-Time Recurrent Neural Network (CTRNN) inspired decay mechanism. Every memory embedding is coupled with a temporal metadata vector `[timestamp, duration, rhythm_phase]`. 

The core algorithm applies an Exponential Decay Function:
`Retrieval_Strength = Base_Salience * e^(-λ * Δt)`
where `λ` is dynamically adjusted based on the emotional/critical weight of the memory, and `Δt` is the elapsed time.

Furthermore, it uses Time-stamped Knowledge Graphs (Temporal KGs) to resolve conflicting facts that change over time (e.g., "User's location is NY (2022)" vs "User's location is SF (2024)"). It implements Allen's Interval Algebra for complex temporal queries (e.g., overlaps, precedes, during).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `query_interval` | `TimeWindow` | The specific span to search. |
| `event_tags` | `list[str]` | Semantic filters. |
| `current_time` | `datetime` | Anchor for decay calculations. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `timeline` | `list[TemporalEvent]` | Chronologically sorted, decay-filtered events. |
| `temporal_conflicts` | `list[Conflict]` | Detected contradictions over time. |

### State Schema
- `event_ledger`: Append-only time-series database of cognitive events.
- `decay_rates`: Matrix of `λ` values for different data categories.

## Dependencies
### Upstream (depends on)
- `H11-SENSOR-FUSION` (Layer 12): Ingests real-time clock and environmental rhythms.
### Downstream (feeds into)
- `H11-EPISODIC-MEM`: Organizes raw episodes onto the timeline.

## Failure Modes
- **Clock Skew**: Desynchronization between distributed sub-agents leading to inverted causality loops.
- **Over-decay**: Important but rarely accessed information drops below the retrieval threshold.
- **Interval Explosion**: Computing Allen's relations across large datasets becomes O(N^2) intractable.

## Performance Characteristics
- Latency: Heavily dependent on the query interval width. Time-series indexing (like TimescaleDB structures) is required.
- Retention: Logarithmic pruning strategy to save space.

## Research References
- Ebbinghaus, H. (1885). "Memory: A Contribution to Experimental Psychology."
- Kazemi, S. M., et al. (2020). "Representation Learning for Dynamic Graphs: A Survey."

## Implementation Notes
Utilize a B-Tree or specialized Time-Series Database (TSDB) for the `event_ledger`. Implement the decay function dynamically at query time rather than continually updating scores in the database to save compute.

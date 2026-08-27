> **Layer 2** · Data Plane & Ingestion · `H11-PROVENANCE`

## Purpose

The H11-PROVENANCE agent provides rigorous tracking of data lineage across the entire substrate. As datasets are crawled, cleaned, curated, and tokenized, this agent records every transformation, maintaining a directed acyclic graph (DAG) of data flow. It exists to answer the critical question: "Exactly which raw bytes contributed to this model, and how were they altered along the way?"

This agent is vital for regulatory compliance (e.g., GDPR's right to explanation, AI Act transparency requirements), debugging data contamination, ensuring reproducibility, and managing intellectual property chains-of-custody.

## Technical Deep-Dive

H11-PROVENANCE implements a specification heavily inspired by OpenLineage and the W3C PROV-O ontology. Lineage is tracked as a graph consisting of `Entities` (datasets, models), `Activities` (jobs, transformations), and `Agents` (users, sub-systems). 

The agent operates asynchronously, ingesting telemetry events emitted by other Layer 2 agents. It stores these events in a graph database (or a specialized relational schema) to enable fast traversal. When a user queries the lineage of a final tokenized dataset, the agent traverses the graph backwards (`wasGeneratedBy` -> `Activity` -> `used` -> `Entity`) to construct a complete provenance tree.

To handle scale, the agent implements graph compaction, rolling up micro-transformations (e.g., row-level filtering) into macro-dataset transitions, while retaining deterministic pointers to the transformation code (via git commits) and parameters used.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `lineage_events` | `List[ProvEvent]` | Stream of transformation events from other agents. |
| `query_entity_id` | `str` | Request to generate lineage for a specific dataset/model. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `provenance_graph` | `ProvGraph` | DAG representing the upstream or downstream lineage. |
| `compliance_report` | `ComplianceDoc` | Formatted report for auditing purposes. |

### State Schema
- `graph_store`: Adjacency list representation of Entities and Activities.
- `unresolved_references`: Temporary holding for events arriving out-of-order.

## Dependencies

### Upstream (depends on)
- All Layer 2 and Layer 3 agents emit events to H11-PROVENANCE.

### Downstream (feeds into)
- `H11-OBSERVE`: For visualizing the lineage graphs in a UI.
- `H11-VERSION`: Links semantic version hashes to provenance nodes.

## Failure Modes
- **Event Dropping**: If the messaging queue is overloaded, missing lineage events result in orphaned graph nodes.
- **Graph Cycle Creation**: Malformed upstream events indicating a dataset depends on itself, breaking DAG traversal.
- **State Bloat**: Storing row-level provenance instead of dataset-level provenance leads to storage exhaustion.

## Performance Characteristics
- **Compute**: Low compute, primarily graph traversal (BFS/DFS).
- **Storage**: High write throughput required for event ingestion; moderate read latency.
- **Latency**: Sub-second resolution for lineage graph generation.

## Research References
- W3C PROV-DM: The PROV Data Model
- "OpenLineage: an Open Standard for Data Lineage"
- "Data Provenance in Machine Learning" (Gebru et al. context)

## Implementation Notes
Use an event sourcing pattern. Entities are immutable; any transformation creates a new Entity. Ensure all event payloads hash their configuration dictionaries to detect silent parameter changes.

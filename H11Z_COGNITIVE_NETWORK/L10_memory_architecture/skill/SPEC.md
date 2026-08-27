> **Layer 10** · Memory Architecture · `H11-SKILL`

## Purpose
The H11-SKILL agent governs procedural memory. While episodic memory stores events and semantic memory stores facts, procedural memory stores *executable code, tools, and programmatic workflows*. It functions as a dynamic library of capabilities that the agent can retrieve, compose, and execute to solve complex tasks.

Inspired by the Voyager architecture in Minecraft, this agent allows the overarching AI to write new code (skills), test them, and if successful, commit them to a persistent library. When faced with novel tasks, it retrieves relevant prerequisite skills and chains them together.

## Technical Deep-Dive
Skills are represented as a Directed Acyclic Graph (DAG) of prerequisites. A skill `DataAnalysis` might depend on `PandasLoader` and `PlotlyVisualizer`. 

The agent utilizes a Dual-Embedding Retrieval System:
1. **Description Embedding**: Retrieves skills based on their natural language docstrings.
2. **Signature Embedding**: Matches I/O types (e.g., if a task needs to output a PDF, it finds skills returning `File[PDF]`).

When a new skill is proposed for insertion, the agent runs an Abstract Syntax Tree (AST) validation and checks for dependency cycles. It employs a dynamic tool-composition engine that dynamically binds arguments between chained skills, acting as a functional orchestrator.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `task_query` | `string` | The task requiring procedural tools. |
| `available_inputs` | `list[Type]` | The data types currently available in the environment. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `executable_plan` | `SkillChain` | A compiled sequence of skill invocations. |
| `missing_prerequisites` | `list[str]` | Skills needed but not present in the library. |

### State Schema
- `skill_registry`: Mapping of skill IDs to executable source code and AST metadata.
- `dependency_graph`: Adjacency matrix tracking which skills call others.

## Dependencies
### Upstream (depends on)
- `H11-TOOL-MAKER` (Layer 9): Generates new Python tools that are ingested here.
### Downstream (feeds into)
- `H11-EXECUTION-ENGINE` (Layer 8): Receives the assembled `SkillChain` for runtime execution.

## Failure Modes
- **Dependency Hell**: Updating a base skill breaks downstream composite skills (requires strict versioning).
- **Security Exploits**: Ingesting procedurally generated skills containing destructive commands (rm -rf).
- **Retrieval Mismatch**: Fetching a visually similar skill that operates on structurally incompatible data.

## Performance Characteristics
- Latency: Very low for retrieval. High for AST validation during insertion.
- Safety: Requires extreme sandboxing and static analysis.

## Research References
- Wang, G., et al. (2023). "Voyager: An Open-Ended Embodied Agent with Large Language Models."
- Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools."

## Implementation Notes
Implement strict semantic versioning for every skill. Use a static type checker (like `mypy` or `pyright` bindings) during the `add_skill` phase to statically guarantee that a composed `SkillChain` will not throw type errors at runtime.

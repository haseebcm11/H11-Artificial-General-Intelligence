> **Layer 5** · Attention & Context Engine · `H11-CONTEXT-WINDOW`

## Purpose
Engineers the context window to mitigate the 'lost-in-the-middle' phenomenon and allocates context budgets for RAG.

This agent ensures optimal performance in Layer 5 by encapsulating deep mathematical mechanics specific to its domain, isolating complex transformations from generic processing flows.

## Technical Deep-Dive
Models degrade in retrieving information from the middle of long contexts. This agent applies context distillation, RAG chunk sorting (e.g., placing highest relevance at sequence edges), and budget allocation among System, User, and Assistant prompt segments to maximize context utilization over 100K+ tokens.

The implementation strictly adheres to theoretical boundaries, avoiding heuristics where deterministic matrices govern the flow. Entropy tracking and structural integrity checks are native to its execution.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| prompt_chunks | List[str] | RAG or conversation chunks |
| max_tokens | int | Budget limit |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| optimized_prompt | str | Reordered/truncated prompt |

### State Schema
- `lost_in_middle_risk`: Risk score of current arrangement

## Dependencies
- **Downstream**: H11-ROPE

## Implementation Notes
Highly optimized pathing. Memory layouts assume continuous tensor spaces where applicable.

> **Layer 22** · Humanities & Social Sciences · `H11-COGNITIVA`

## Purpose

H11-COGNITIVA models the functional architecture of the mind, abstracting biological neural networks into high-level cognitive processes (working memory, attention, executive function). It acts as the bridge between raw neurobiology (H11-NEUROSCIENTIA) and subjective psychology (H11-PSYCHOLOGIA).

## Technical Deep-Dive

The agent implements an ACT-R (Adaptive Control of Thought-Rational) inspired cognitive architecture. Declarative memory is modeled via spreading activation networks, while procedural memory relies on production rule compilation.

Attention is calculated using a saliency map governed by a Bayesian surprise metric. Cognitive bottlenecks are explicitly enforced by bounding the working memory capacity (the "magical number 4±1" chunk limit).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sensory_buffer | Dict[str, Any] | Raw perceptual inputs |
| current_goal | str | Executive target |
| memory_query | str | Retrieval prompt |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| attention_focus | str | The most salient input node |
| working_memory | List[str] | Current active chunks |
| cognitive_load | float | Percentage of capacity used |

### State Schema
Maintains `CognitiveWorkspace`, containing the declarative network and procedural rule sets.

## Dependencies

### Upstream (depends on)
H11-NEUROSCIENTIA, H11-PSYCHOLOGIA

### Downstream (feeds into)
H11-EDUCATION, H11-EXISTENTIA

## Failure Modes
1. Attentional Blink (rapid succession of high-saliency inputs causes total drop of the second stimulus).
2. Thrashing (goal switching occurs faster than procedural compilation).

## Performance Characteristics
Requires rapid graph-traversal for spreading activation and constant cache evictions to simulate forgetting curves.

## Research References
- Anderson, J. R. (2007). How Can the Human Mind Occur in the Physical Universe? (ACT-R).
- Cowan, N. (2001). The magical number 4 in short-term memory.

## Implementation Notes
Use an LRU (Least Recently Used) cache coupled with a time-based decay function to faithfully model working memory limitations.

> **Layer 6** · Sequence & State-Space Engine · `H11-PREFIX`

## Purpose

The H11-PREFIX agent injects continuous virtual tokens (soft prompts) into sequence architectures. It manages P-tuning and prefix-tuning paradigms, allowing the substrate to condition generative trajectories based on task-specific, learned embeddings rather than discrete text prompts.

## Technical Deep-Dive

Traditional prompting uses discrete tokens mapped through an embedding layer. H11-PREFIX maintains a library of parameter-efficient fine-tuned continuous representations (Prefixes). These vectors bypass the embedding layer and are directly concatenated with the keys and values at every attention layer (Prefix Tuning) or just at the input layer (Prompt Tuning).

The agent handles prefix composition, dynamically combining multiple virtual tokens (e.g., an "Instruction" prefix and a "Style" prefix) by performing weighted summation or concatenation in the latent space before passing them to the main sequence processor.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| task_id | str | Identifier for the soft prompt |
| sequence_embeddings | List[List[float]] | The actual input data |
| prefix_mode | str | 'input_only' or 'all_layers' |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| conditioned_sequence | List[List[float]] | Sequence prepended with prefixes |
| prefix_tensors | Dict[str, List[float]] | KV matrices for attention |

### State Schema
Caches loaded soft prompt matrices in GPU memory for fast swapping.

## Dependencies
- Upstream: None (Acts as a side-channel injector)
- Downstream: H11-SEQUENCE

## Failure Modes
- EmbeddingDrift: Soft prompts trained on base model version A degrading violently on version B.
- ContextStarvation: Exceedingly long continuous prefixes eating up the generation context window.

## Research References
- Prefix-Tuning: Optimizing Continuous Prompts for Generation
- The Power of Scale for Parameter-Efficient Prompt Tuning (Lester et al.)

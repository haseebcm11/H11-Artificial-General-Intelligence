> **Layer 6** · Sequence & State-Space Engine · `H11-LONGCONTEXT`

## Purpose

The H11-LONGCONTEXT agent systematically expands the effective receptive field of sequence models beyond traditional context window limits. It coordinates various context extension strategies, such as Rotary Position Embedding (RoPE) scaling, landmark attention mechanisms, and context compression, enabling models to reason over hundreds of thousands or millions of tokens.

## Technical Deep-Dive

Extending context isn't just about larger memory buffers; it requires manipulating the frequency components of positional embeddings to extrapolate beyond training lengths. This agent implements YaRN (Yet another RoPE extensioN method) and dynamic NTK-aware scaling. 

Furthermore, it integrates "Infini-attention" style memory compression, taking older sequence chunks and continually projecting them into a fixed-size associative memory matrix (analogous to a continuous Hopfield network), seamlessly merging short-term precise attention with long-term compressed retrieval within the same processing stream.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| position_ids | List[int] | Absolute position indices |
| scaling_factor | float | Required context multiplier |
| context_mode | ContextMode | 'rope_scaling', 'landmark', 'compressed' |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| scaled_positions | List[float] | Adjusted frequency bases |
| compression_masks | List[bool] | Tokens designated for memory sink |

### State Schema
Tracks the continuously updated associative memory matrix $M \in \mathbb{R}^{D 	imes D}$.

## Dependencies
- Upstream: H11-SEQUENCE
- Downstream: None

## Failure Modes
- FrequencyClash: Interpolating too aggressively causing high-frequency information loss.
- CompressionBleed: Sinking critical exact-match tokens into fuzzy associative memory.

## Research References
- YaRN: Efficient Context Window Extension of Large Language Models
- Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention

> **Layer 6** · Sequence & State-Space Engine · `H11-CAUSAL-MASK`

## Purpose

The H11-CAUSAL-MASK agent strictly enforces autoregressive properties by generating and manipulating attention masks. It prevents information leakage from future tokens into current states during parallel training, handling lower-triangular causal masks, prefix-LM bidirectional masking, and document-boundary masking.

## Technical Deep-Dive

Causal masking in standard transformers requires materializing an $N 	imes N$ matrix of $-\infty$ values above the diagonal. To optimize memory, this agent constructs implicit boolean mask representations or sparse tensor indices that avoid allocating $O(N^2)$ memory natively. 

It uniquely supports "Prefix-LM" masking algorithms, where a designated prefix (e.g., prompt or context) is allowed full bidirectional attention, while the subsequent generation tokens remain strictly causal. It also integrates with H11-CHUNKING to prevent cross-document attention within a single packed batch.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| sequence_length | int | Target N dimension |
| mask_type | MaskType | 'strict_causal', 'prefix_lm', 'document_blocked' |
| prefix_length | Optional[int] | Length of bidirectional prefix |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| boolean_mask | List[List[bool]] | For standard attention |
| sparse_indices | List[Tuple[int, int]] | For sparse attention |

### State Schema
Stateless by design, but caches frequently used sizes (e.g., 2048x2048).

## Dependencies
- Upstream: H11-SEQUENCE
- Downstream: Attention modules

## Failure Modes
- FutureLeakage: Incorrect offsets allowing position $i$ to attend to $i+1$.
- DiagonalSparsity: Masking out the diagonal, preventing a token from attending to itself.

> **Layer 10** · Memory Architecture · `H11-COMPRESSION-MEM`

## Purpose
The H11-COMPRESSION-MEM agent manages the system's token budget by recursively synthesizing, compressing, and distilling long-form context into dense semantic representations. As agents interact, raw dialogue and operational logs quickly exceed fixed LLM context windows. This agent prevents context exhaustion by maintaining a tiered compression hierarchy.

It acts as an "Attention Sink" manager, ensuring that crucial initial prompts and foundational system instructions remain perfectly preserved, while intermediate conversational turns and older procedural logs are subjected to lossy compression.

## Technical Deep-Dive
The agent utilizes an Iterative Context Distillation (ICD) algorithm. It processes token streams into chunks, identifying low-information-density segments using a pre-calculated surprisal metric. 

It implements a dual-tier architecture:
1. **Extractive Compression**: Uses keyphrase extraction and selective deletion (inspired by LLMLingua) to remove redundant adjectives, stop words, and predictable tokens while maintaining perplexity bounds.
2. **Abstractive Compression**: Uses a specialized summarization prompt to rewrite lengthy passages into highly dense propositional logic or bulleted summaries.

Furthermore, it explicitly supports Attention Sinks (StreamingLLM framework), dedicating the first 4-8 tokens of any compressed representation to stable sink tokens, ensuring that downstream LLMs maintain stable attention maps even when evaluating highly compressed contexts.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `raw_text_blocks` | `list[TextBlock]` | Sequence of texts to compress. |
| `target_token_budget` | `int` | The maximum allowable size of the output. |
| `preservation_keys` | `list[str]` | Entities or terms that must survive compression. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `compressed_context` | `string` | The distilled text block. |
| `compression_ratio` | `float` | Original size / New size. |
| `lost_entities` | `list[str]` | Minor details lost during abstractive compression. |

### State Schema
- `compression_cache`: Hash map of previously compressed blocks and their summaries.
- `attention_sinks`: Preserved global structural tokens.

## Dependencies
### Upstream (depends on)
- `H11-EPISODIC-MEM`: Compresses old episodes before archiving.
- `H11-WORKING-MEM`: Shrinks working memory when context limits approach.
### Downstream (feeds into)
- `H11-ROUTER`: Provides condensed context for task routing.

## Failure Modes
- **Semantic Drift**: Repeated recursive summarization distorts the original meaning (the "telephone game" effect).
- **Entity Erasure**: Over-aggressive compression drops critical variables or identifiers.
- **Catastrophic Forgetting**: Loss of context continuity if the transition between chunks is not smoothed.

## Performance Characteristics
- Compute: Heavy (requires evaluating perplexity/surprisal for extractive compression).
- Throughput: High, designed for stream processing.

## Research References
- Jiang, H., et al. (2023). "LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models."
- Xiao, G., et al. (2023). "Efficient Streaming Language Models with Attention Sinks."

## Implementation Notes
Implement token estimation using a fast tokenizer (e.g., tiktoken). The extractive step should use a lightweight local model or heuristic to avoid costly API calls, reserving the abstractive summarization for when extractive compression fails to meet the target budget.

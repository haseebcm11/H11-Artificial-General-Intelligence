> **Layer 2** · Data Plane & Ingestion · `H11-FILTER`

## Purpose

The H11-FILTER agent operates as the surgical removal instrument of the Data Plane. While H11-QUALITY assesses macroscopic dataset health, H11-FILTER performs fine-grained, row-level eradication of toxic, redundant, or otherwise deleterious content. Its primary mission is twofold: enforcing policy constraints (e.g., removing Hate Speech, PII, NSFW content, and copyright-encumbered materials) and executing extreme-scale deduplication.

Training state-of-the-art models on duplicated data leads to memorization, reduced generalization, and wasted compute. This agent ensures maximum information density per token by obliterating exact matches and near-duplicates before they reach the augmentation or synthesis phases. Furthermore, it incorporates perplexity-based filtering to discard machine-generated spam, scraper artifacts, and incoherent text.

## Technical Deep-Dive

Deduplication in H11-FILTER utilizes a two-tiered architecture. Exact deduplication relies on massive, distributed Bloom Filters configured with ultra-low false positive rates (e.g., $10^{-7}$). For the far more complex task of near-deduplication, the agent implements the MinHash algorithm with Locality-Sensitive Hashing (LSH). It tokenizes text into n-grams, computes min-hashes across dozens of permutation functions, and groups signatures into LSH bands. If two documents collide in any band, they are evaluated for exact Jaccard similarity, and the redundant graph edges are pruned using Union-Find to retain only the highest-quality node in a connected component.

Policy filtering relies on a cascade of progressively heavier classifiers. It starts with deterministic fast-paths (regex blocklists and Aho-Corasick automaton for rapid keyword matching). Documents surviving the fast-path are subjected to KenLM (a highly optimized N-gram language model) which computes document perplexity. Texts with abnormally high perplexity (random noise) or abnormally low perplexity (repetitive spam) are excised. Finally, borderline content is routed to lightweight Transformer-based classifiers (e.g., DistilRoBERTa) trained for NSFW and toxic content detection.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `documents` | `List[ContentPayload]` | Unfiltered stream of text or multimodal records. |
| `policy_profile` | `FilterPolicy` | Thresholds for toxicity, perplexity, and dedup strictness. |
| `lsh_config` | `LSHParams` | Tuning parameters for MinHash bands and permutations. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `clean_documents` | `List[ContentPayload]` | Documents surviving all filter stages. |
| `pruned_ids` | `List[str]` | IDs of dropped documents. |
| `filter_telemetry` | `FilterMetrics` | Counters tracking which pipeline stage dropped what. |

### State Schema
- `bloom_filter_state`: In-memory byte arrays representing the exact-match hashes.
- `lsh_index`: Banded hash tables for near-duplicate collision detection.
- `trie_blocklist`: Compiled Aho-Corasick automaton for $O(N)$ string matching.

## Dependencies

### Upstream (depends on)
- `H11-QUALITY`: Ensures the batch is worth processing before burning compute on deduplication.

### Downstream (feeds into)
- `H11-AUGMENTER`: Consumes clean, unique data for perturbation.
- `H11-SYNTHDATA`: Avoids synthesizing data that mimics filtered/toxic distributions.

## Failure Modes
1. **LSH Hash Collisions**: Poorly tuned bands/rows resulting in excessive false positive near-duplicates, accidentally deleting unique, valuable training data.
2. **KenLM Distribution Mismatch**: Perplexity filtering on domain-specific data (e.g., genetic sequences, heavy math) causing it to be incorrectly flagged as random noise.
3. **Filter Starvation**: Overly aggressive safety classifiers creating an artificially sanitized dataset that harms model capability and representation.
4. **Union-Find Memory Bloat**: Keeping massive duplicate connected-components in memory before pruning, leading to OOM on billion-document corpora.

## Performance Characteristics
- MinHash Signature Generation: ~2MB/s per CPU core.
- Bloom Filter lookups: $O(k)$ time, typically nanoseconds per document.
- Safety Classifiers: ~500 seq/s batched on GPU.

## Research References
- Broder, A. Z. (1997). On the resemblance and containment of documents (MinHash).
- Leskovec, J., Rajaraman, A., & Ullman, J. D. (2020). Mining of Massive Datasets (Locality-Sensitive Hashing).
- Wenzek, G., et al. (2019). CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data.

## Implementation Notes
When constructing the LSH index, ensure the number of bands $b$ and rows $r$ satisfies the threshold approximation $t \approx (1/b)^{1/r}$. Set $t$ to around 0.8 to target documents that are highly semantically overlapping. Implement the Bloom Filter using MurmurHash3 for optimal dispersion and speed.

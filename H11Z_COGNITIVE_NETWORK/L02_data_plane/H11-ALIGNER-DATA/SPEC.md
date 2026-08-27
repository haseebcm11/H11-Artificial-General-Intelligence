> **Layer 2** · Data Plane & Ingestion · `H11-ALIGNER-DATA`

## Purpose

The H11-ALIGNER-DATA agent serves as the core registration engine for disjoint, asynchronous, or multi-modal data streams entering the H11 Cognitive Substrate. In advanced machine learning systems, data is rarely perfectly synchronized at ingestion. Whether it's parallel bilingual corpora needing sentence-level alignment, audio tracks requiring exact timestamp mapping to transcripts, or multi-view visual inputs requiring spatial registration, this agent performs the computational heavy lifting to synchronize them into coherent tuple structures.

By providing a unified interface for data pairing, the H11-ALIGNER-DATA agent ensures that subsequent modeling layers receive tightly coupled, contextually bounded sequences. It acts as the critical bridge between raw, unstructured multimodality and structured, co-referenced training pairs, significantly reducing the "alignment tax" incurred during late-fusion processes.

## Technical Deep-Dive

Data alignment within this agent employs distinct algorithmic paradigms depending on the modalities involved. For text-to-text (parallel corpora), it implements a modernized Gale-Church algorithm enhanced with neural embeddings. While the classical Gale-Church uses length-based statistical heuristics (assuming longer sentences in L1 translate to longer sentences in L2), our neural variant incorporates cosine similarity over cross-lingual representations (e.g., LaBSE or multilingual BERT) to resolve 1:N, N:1, and N:M alignments precisely.

For temporal alignment, specifically audio-to-text, the agent leverages Connectionist Temporal Classification (CTC) forced alignment. Instead of relying on manual timestamps, it utilizes acoustic models to predict frame-level phoneme probabilities and applies a dynamic programming Viterbi decoder to find the optimal monotonic alignment path between the acoustic frames and the known transcript characters. This enables precise millisecond-level bounding boxes for words and phonemes.

For continuous numerical streams or misaligned time-series data, it utilizes generalized Dynamic Time Warping (DTW) with FastDTW constraints. The DTW algorithm recursively computes the optimal nonlinear warping path between two sequences by minimizing the cumulative Euclidean distance in a local cost matrix, restricted by a Sakoe-Chiba band to maintain $O(N)$ computational complexity instead of $O(N^2)$.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `primary_stream` | `List[DataItem]` | The anchor modality or reference sequence. |
| `secondary_stream` | `List[DataItem]` | The target modality or sequence to align against the anchor. |
| `modality_pair` | `ModalityPairType` | Enum specifying text-text, audio-text, or series-series. |
| `alignment_strategy` | `AlignmentStrategy` | Algorithm choice (e.g., `GALE_CHURCH`, `CTC_FORCED`, `DTW`). |
| `tolerance_window` | `float` | Maximum permitted temporal/spatial divergence. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `aligned_pairs` | `List[AlignedTuple]` | The synchronized mappings with confidence scores. |
| `unaligned_orphans` | `List[DataItem]` | Items from either stream that could not be confidently paired. |
| `alignment_density` | `float` | Ratio of aligned vs total items (useful for quality gating). |
| `global_cost` | `float` | The overall alignment cost (e.g., DTW cumulative distance). |

### State Schema
- `active_alignments`: Tracks in-flight alignment jobs for massive datasets.
- `embedding_cache`: LRU cache for cross-lingual embeddings to prevent redundant neural passes.
- `acoustic_model_state`: Lazy-loaded weights for CTC alignment models.

## Dependencies

### Upstream (depends on)
- `H11-INGEST`: Provides raw streams of unbounded data.
- `H11-NORMALIZER`: Ensures text or audio is pre-processed (tokenized/resampled) before alignment.

### Downstream (feeds into)
- `H11-QUALITY`: Assesses the alignment density and drops poorly aligned batches.
- `H11-TRAINER`: Consumes the perfectly paired data for multimodal representation learning.

## Failure Modes
1. **Catastrophic Monotonicity Failure**: In DTW, extreme warping paths where one frame maps to thousands of target frames, signaling fundamentally unrelated sequences.
2. **CTC Decoding Collapse**: Acoustic model fails to spike on correct phonemes due to heavy background noise, causing Viterbi backtracking to fail.
3. **Cross-lingual Divergence**: Gale-Church failing on idiomatic translations where length distributions and semantic embeddings completely mismatch.
4. **OOM on Unbanded DTW**: Passing excessively long sequences without a proper Sakoe-Chiba radius, exceeding GPU memory allocations.

## Performance Characteristics
- DTW throughput: ~500k frames/sec per core using FastDTW approximations.
- Neural Gale-Church: ~10k sentence pairs/sec batched on GPU.
- CTC Alignment: Near real-time (< 0.1x RTF) on CPU.

## Research References
- Gale, W. A., & Church, K. W. (1993). A program for aligning sentences in bilingual corpora.
- Graves, A., et al. (2006). Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks.
- Salvador, S., & Chan, P. (2007). Toward accurate dynamic time warping in linear time and space.

## Implementation Notes
When implementing FastDTW, ensure the search radius is dynamically adjusted based on the variance of the local sampling rate. For CTC, pre-compute the log-probability matrix and reuse it across multiple forced alignment hypotheses if the transcript has slight variations.

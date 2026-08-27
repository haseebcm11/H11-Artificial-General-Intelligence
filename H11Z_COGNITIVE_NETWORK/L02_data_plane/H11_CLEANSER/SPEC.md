> **Layer 2** · Data Plane & Ingestion · `H11-CLEANSER`

## Purpose

Data arriving from external environments is fundamentally chaotic. H11-CLEANSER ensures substrate-wide data hygiene by rigorously normalizing, deduplicating, and repairing inbound datasets before they enter active memory loops.

This agent operates over high-dimensional datasets, applying statistical anomaly detection and metric-space deduplication. It resolves missing values through localized context imputation and enforces strict encoding uniformity (e.g., standardizing UTF-8 and coercing untyped variables).

## Technical Deep-Dive

Deduplication at scale relies on MinHash Locality-Sensitive Hashing (LSH). Instead of pairwise $O(N^2)$ comparisons, documents are tokenized via k-shingling. A family of universal hash functions generates a compact MinHash signature. Documents colliding in LSH buckets are then evaluated for Jaccard similarity, resolving near-duplicates in $O(N)$ expected time.

For outlier detection, H11-CLEANSER employs Isolation Forests. Anomalies are isolated closer to the root of random decision trees. Records with an anomaly score exceeding an adaptive threshold (dynamically calibrated via extreme value theory) are quarantined.

Missing value imputation utilizes a K-Nearest Neighbors (KNN) algorithm modified for categorical proximity, augmented by an Iterative Imputer (MICE) for continuous multivariate feature matrices, ensuring the variance distribution remains stable.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `raw_corpus` | `DataFrame / Stream` | Unclean data payloads |
| `dedup_threshold`| `float` | Jaccard similarity threshold for deletion (e.g., 0.95) |
| `imputation_mode`| `ImputeStrategy` | `KNN`, `MEAN`, `MICE`, `DROP` |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `clean_corpus` | `DataFrame / Stream` | Normalized data |
| `quarantine` | `List[Record]` | Records failing structural validation |
| `cleansing_metrics`| `CleansingStats` | Count of imputed/dropped rows |

### State Schema
- `lsh_index`: Persistent memory structure grouping MinHash bands.
- `distribution_profiles`: Moving averages of feature variances for drift detection.
- `quarantine_logs`: Append-only history of removed anomalies.

## Dependencies

### Upstream (depends on)
- `H11-INGEST`, `H11-CRAWLER`: Provide the raw inputs.

### Downstream (feeds into)
- `H11-LABELER`: Requires pristine data to avoid wasting human/machine annotation effort.
- `H11-EMBEDDER` (Layer 3): Needs clean text for semantic vectorization.

## Failure Modes
1. **LSH Bucket Overflow**: A highly repetitive corpus clusters into a single bucket, collapsing performance back to $O(N^2)$. Handled by dynamic band resizing.
2. **Imputation Hallucination**: MICE algorithm invents high-leverage data points due to collinearity in features.
3. **Encoding Coercion Loss**: Destructive UTF-8 normalization obliterating rare CJK mathematical symbols.

## Performance Characteristics
- **Throughput**: Processes 100k rows/second on CPU for standard text cleansing.
- **LSH Overhead**: Hashing introduces a latency of ~1ms per document.

## Research References
- "Mining of Massive Datasets" (Leskovec, Rajaraman, Ullman) - MinHash LSH.
- "Isolation Forest" (Liu, Ting, Zhou, ICDM 2008).
- "Multiple Imputation by Chained Equations (MICE)" (Azur et al.).

## Implementation Notes
Implement LSH bands using matrix operations in NumPy to avoid Python loop overhead. Isolation Forest can utilize scikit-learn bindings if available, otherwise construct a simplified binary tree ensemble.

> **Layer 2** · Data Plane & Ingestion · `H11-CURATOR`

## Purpose

The H11-CURATOR agent orchestrates the composition, mixing, and ordering of large-scale pretraining datasets. It is responsible for taking a diverse set of upstream corpora and applying advanced data selection strategies such as Importance Resampling (DSIR) and Diverse Data Distribution (D4) to create optimal training mixtures. It ensures that the final dataset represents the targeted distribution while mitigating benchmark leakage through rigorous decontamination.

By defining curriculum ordering, the H11-CURATOR agent significantly accelerates model convergence. It acts as the intelligent sieve that separates high-utility tokens from noisy or redundant data, directly impacting the final downstream performance of the trained models.

## Technical Deep-Dive

Curating a multi-terabyte dataset requires shifting from heuristic domain weights to principled, algorithm-driven data selection. The H11-CURATOR utilizes Data Selection with Importance Resampling (DSIR), which approximates the target distribution by reweighting data from large, diverse pools (like Common Crawl) to match a smaller, high-quality reference set (e.g., Wikipedia + scientific papers). This involves computing influence functions or lightweight n-gram language models over both the target and source distributions, calculating importance weights, and resampling accordingly.

For benchmark decontamination, the agent employs a scalable rolling-hash Bloom filter approach. It constructs an n-gram index of all evaluation benchmarks and flags training sequences that exhibit significant overlap (e.g., 13-gram exact match) with the evaluation set. To handle the scale, it distributes this check across partitioned Bloom filters.

Curriculum ordering is managed via a pacing function. The agent constructs a localized data loader schedule where initial epochs heavily sample structurally simple, high-quality data (e.g., encyclopedic text), gradually introducing harder, noisier data (e.g., raw web scrapes and complex code). This is modeled as a time-varying probability density function over the data domains.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `target_distribution_refs` | `List[DatasetRef]` | References to high-quality datasets to emulate. |
| `source_pools` | `List[DatasetRef]` | Large, uncurated data pools available for sampling. |
| `benchmark_sets` | `List[DatasetRef]` | Evaluation sets for decontamination. |
| `curriculum_config` | `CurriculumConfig` | Parameters defining the pacing function. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `curated_manifest` | `DatasetManifest` | Ordered list of selected document URIs/offsets. |
| `mixing_ratios` | `Dict[str, float]` | Final computed sampling weights per domain. |
| `decontamination_report` | `DeconReport` | Statistics on dropped documents due to overlap. |

### State Schema
- `dsir_lms`: State of the lightweight language models used for importance weighting.
- `bloom_filters`: Serialized Bloom filters of benchmark n-grams.
- `curriculum_step`: Current global step in the curriculum pacing function.

## Dependencies

### Upstream (depends on)
- `H11-CORPUS`: Provides the raw, parsed document pools.
- `H11-EVAL`: Provides the benchmark datasets for decontamination.

### Downstream (feeds into)
- `H11-SHARDER`: Takes the curated manifest to partition it for distributed training.

## Failure Modes
- **Mode Collapse in DSIR**: Resampling too greedily from a narrow subset, leading to catastrophic forgetting of broader domains.
- **Over-decontamination**: Accidentally filtering out fundamental linguistic constructs if the benchmark n-gram threshold is too low.
- **Curriculum Stagnation**: Pacing function transitions too slowly, causing the model to overfit on the "easy" initial data.

## Performance Characteristics
- **Compute**: Heavy CPU bound during n-gram LM training and Bloom filter construction.
- **Memory**: Requires large RAM footprint (e.g., 256GB+) to hold distributed Bloom filters and suffix arrays for decontamination.
- **Throughput**: Can process and score ~10TB of text per hour per node.

## Research References
- Xie et al., "Data Selection for Language Models via Importance Resampling" (DSIR)
- Tirumala et al., "D4: Improving LLM Pretraining via Diverse Data Distribution"
- Marion et al., "When Less is More: Investigating Data Pruning for Pretraining"

## Implementation Notes
Use `pyahocorasick` or custom Rust bindings for efficient exact string matching during decontamination. DSIR weights should be computed on a heavily downsampled subset of the source pool to maintain computational feasibility.

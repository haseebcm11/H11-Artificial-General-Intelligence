> **Layer 2** · Data Plane & Ingestion · `H11-QUALITY`

## Purpose

The H11-QUALITY agent functions as the principal sentinel within the Data Plane, responsible for computing multi-dimensional quality scores and enforcing Data Level Agreements (DLAs) across incoming datasets. Raw data inevitably carries noise, biases, structural anomalies, and distributional shifts. In an AGI substrate, injecting low-fidelity data cascades into severe model degradation. This agent programmatically quantifies data integrity before it enters training or analytical layers.

Rather than simple schema validation, H11-QUALITY acts on the Wang & Strong ontological framework of data quality, measuring Intrinsic (accuracy), Contextual (relevancy, timeliness), Representational (format consistency), and Accessibility properties. It operates as an automated gatekeeper, quarantining degraded batches, generating comprehensive statistical drift profiles, and executing programmatic Data Contracts to ensure SLAs are explicitly fulfilled by upstream ingestion providers.

## Technical Deep-Dive

To quantify structural and statistical integrity, the agent computes a series of non-parametric tests. For distribution drift detection over continuous variables, it leverages the two-sample Kolmogorov-Smirnov (KS) test and the Wasserstein metric (Earth Mover's Distance). These measure the maximum divergence between the empirical cumulative distribution functions (ECDF) of an incoming batch versus a historical baseline, robustly identifying feature drift without assuming underlying gaussian distributions.

For text data, the agent computes intrinsic accuracy proxies such as compression ratios, entropy measures, and vocabulary richness (Type-Token Ratio or Yule's I). Contextual timeliness is verified through temporal contract bounds. The data contract enforcement is implemented via an extensible Directed Acyclic Graph (DAG) of quality predicates. Each dataset is bound by a DLA specifying acceptable bounds for completeness (ratio of non-null vectors), uniqueness, and semantic consistency. If a batch violates a critical predicate (a "hard gate"), the data is atomically rejected, and the agent emits a circuit-breaking event to upstream pipelines.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `dataset_batch` | `DataBatch` | Multi-dimensional array or dataframe of incoming records. |
| `data_contract` | `QualityContract` | Declarative SLA outlining thresholds for dimensions. |
| `baseline_stats` | `StatisticalProfile` | Historical ECDF and moments for drift comparison. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `overall_score` | `float` | Aggregate Wang & Strong quality index (0.0 to 1.0). |
| `dimension_scores` | `Dict[str, float]` | Granular scores across quality dimensions. |
| `drift_metrics` | `List[DriftAlert]` | Detected statistical divergences vs baseline. |
| `gate_status` | `GateDecision` | PASSED, QUARANTINED, or REJECTED. |

### State Schema
- `historical_profiles`: Exponentially decayed moving averages of dataset statistics.
- `contract_registry`: Active Data Level Agreements indexed by dataset URI.
- `quarantine_zone`: Pointers to datasets temporarily withheld for human review.

## Dependencies

### Upstream (depends on)
- `H11-INGEST`: Supplies raw batched data.
- `H11-ALIGNER-DATA`: Supplies alignment density metrics which feed into completeness scores.

### Downstream (feeds into)
- `H11-FILTER`: Downstream cleaning only runs on data that passes basic quality gates.
- `H11-MONITORING` (Layer 6): Receives real-time drift alerts.

## Failure Modes
1. **False Positive Drift Alarm**: Seasonal or expected distribution shifts triggering the KS-test, causing massive unnecessary quarantine.
2. **Contract Impasse**: Overly strict Data Contracts rendering ingestion impossible (0% pass rate).
3. **Statistical Profile Corruption**: Baseline stats contaminated by undetected poisoning, causing the agent to accept adversarial noise.
4. **Compute Bottleneck**: Calculating Wasserstein distance on extremely high-dimensional embedding spaces exceeding latency SLAs.

## Performance Characteristics
- Fast Predicate Evaluation: >100k rows/sec for null/type checks.
- Statistical Profiling: 10k rows/sec for 1D KS-tests and Wasserstein.
- Memory: Low operational footprint, strictly bounded by sample size limits for ECDF estimation.

## Research References
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers.
- Arjovsky, M., Chintala, S., & Bottou, L. (2017). Wasserstein GAN (for Earth Mover's Distance theory).
- Massey, F. J. (1951). The Kolmogorov-Smirnov test for goodness of fit.

## Implementation Notes
To manage high-dimensional data, apply Principal Component Analysis (PCA) projection before computing Wasserstein distances. Implement Data Contracts using a composable rule engine (like a lightweight Python AST evaluator) to allow hot-reloading of SLA conditions without restarting the agent.

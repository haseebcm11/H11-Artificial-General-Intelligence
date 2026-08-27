> **Layer 2** · Data Plane & Ingestion · `H11-SAMPLER`

## Purpose

The H11-SAMPLER agent is responsible for dynamically sub-selecting, over-sampling, and re-weighting datasets ingested into the cognitive substrate. In large-scale model training and data analysis, raw data distributions are frequently skewed, long-tailed, or misaligned with the learning objective. H11-SAMPLER remedies this by applying advanced statistical sampling techniques.

By dynamically altering the data stream, H11-SAMPLER can prioritize hard examples (Active Learning), balance minority classes (SMOTE/ADASYN), or smoothly transition from simple to complex examples (Curriculum-based). Its role is foundational to ensuring that the neural pathways in downstream layers receive optimal learning signals.

## Technical Deep-Dive

H11-SAMPLER employs multiple sophisticated sampling algorithms. For infinite or extremely large streams, it uses Reservoir Sampling (Algorithm R and Algorithm L) to maintain a representative uniformly distributed sample over a streaming input of unknown size, executing in O(n) time and O(k) memory. 

For handling class imbalance in continuous vector spaces, it implements SMOTE (Synthetic Minority Over-sampling Technique) and ADASYN (Adaptive Synthetic Sampling). ADASYN improves upon SMOTE by using a weighted distribution for different minority class examples according to their level of difficulty in learning, mathematically defined as a density ratio of majority to minority instances in a k-NN neighborhood.

In curriculum learning modes, the agent utilizes a dynamic temperature-based scaling function: P(x) = exp(-C(x)/T) / Z, where C(x) is the complexity score of the datum, T is the temperature parameter decaying over time, and Z is the partition function. This allows the network to initially focus on simple data (high T limits the effect of complexity) and gradually shift to complex data as T approaches 0.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| data_batch | List[Dict] | Raw input data items with features and optional labels |
| sampling_strategy | String | The chosen strategy (e.g., 'smote', 'reservoir', 'curriculum') |
| current_epoch | Integer | Used for time-decaying sampling like curriculum |
| complexity_scores | Map[String, Float] | Required for active learning or curriculum sampling |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| sampled_batch | List[Dict] | The modified, sub-selected or synthetically augmented data |
| weights | List[Float] | Importance weights for each sampled item to correct bias |
| effective_ratio | Float | The ratio of output items to input items |

### State Schema
The agent maintains `SamplingState` which includes `ReservoirBuffer` (for stream sampling), `ClassDistribution` (moving averages of class frequencies), and `CurriculumTemperature` (current epoch T value).

## Dependencies

### Upstream (depends on)
H11-STREAMING-DATA (provides raw stream chunks), H11-ETL-DATA (provides normalized historical data).

### Downstream (feeds into)
H11-L3-TRAINERS (consumes the balanced/sampled batches).

## Failure Modes
1. **Mode Collapse in Synthetic Sampling**: Over-generating synthetic points in a sparse region.
2. **Buffer Overflow**: Reservoir memory limits exceeded in extreme k configurations.
3. **Weight Explosion**: Importance sampling weights becoming NaN due to zero-probability denominators.

## Performance Characteristics
Optimized for high-throughput vectorized operations. Synthetic generation (SMOTE) requires k-NN searches, bounding throughput to ~10k ops/sec per CPU core, whereas reservoir sampling operates at ~500k ops/sec.

## Research References
- Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique."
- He, H., et al. (2008). "ADASYN: Adaptive synthetic sampling approach for imbalanced learning."
- Bengio, Y., et al. (2009). "Curriculum learning."

## Implementation Notes
Use vectorized NumPy/CuPy operations for k-NN computations in SMOTE. Ensure random seeds are deterministic and check-pointed for reproducibility during distributed training.

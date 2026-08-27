> **Layer 2** · Data Plane & Ingestion · `H11-LABELER`

## Purpose

Unlabeled raw data has limited utility for supervised cognitive paradigms. H11-LABELER bridges the semantic gap by attaching structured taxonomies and high-confidence annotations to the data stream. It manages the entire labeling lifecycle: programmatic weak supervision, active learning sampling, and inter-annotator agreement tracking.

Rather than exhaustively labeling every data point, H11-LABELER optimizes labeling budgets. It uses algorithmic uncertainty to request human intervention only for the most informative edge cases, while programmatically auto-labeling the rest using heuristics and generative models.

## Technical Deep-Dive

The core of programmatic labeling leverages a Snorkel-inspired Data Programming approach. Users define Labeling Functions (LFs)—noisy, heuristic rules. H11-LABELER constructs a Generative Label Model that estimates the accuracies and correlations of these LFs without ground truth, outputting a probabilistic label distribution for each record.

For Active Learning, the agent uses Entropy-based Uncertainty Sampling. Given a preliminary classifier, it queries records $x$ that maximize Shannon entropy: $H(y|x) = - \sum P(y_i|x) \log P(y_i|x)$. 

When crowdsourced or expert human annotators provide labels, the agent computes Krippendorff's Alpha to measure inter-annotator reliability. Unlike Cohen's Kappa, Krippendorff's Alpha generalizes across missing data, multiple annotators, and various metric levels (nominal, ordinal, interval), making it robust for distributed asynchronous annotation workflows.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `unlabeled_pool` | `Dataset` | High-quality dataset from H11-CLEANSER |
| `labeling_functions`| `List[Callable]` | Heuristic rules for weak supervision |
| `taxonomy` | `Tree[LabelNode]` | Hierarchical definition of valid classes |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `probabilistic_labels`| `Matrix` | Soft labels (distributions over classes) |
| `active_queries` | `List[Record]` | Subset requiring human intervention |
| `agreement_score` | `float` | Krippendorff's alpha for current annotations |

### State Schema
- `lf_empirical_accuracies`: Estimated weights of heuristic functions.
- `annotation_ledger`: Append-only log of who labeled what and when.
- `class_priors`: Base rates of taxonomy classes.

## Dependencies

### Upstream (depends on)
- `H11-CLEANSER`: Guarantees input data is deduplicated.

### Downstream (feeds into)
- `H11-TRAINER` (Layer 4): Consumes labeled datasets for model fine-tuning.

## Failure Modes
1. **Correlated LF Collapse**: Multiple labeling functions use the exact same underlying signal, deceiving the generative model into overconfidence.
2. **Sampling Bias**: Uncertainty sampling completely ignores "easy" examples, skewing the decision boundary during model training. (Mitigated by $\epsilon$-greedy random sampling).
3. **Annotator Collusion**: Crowdsourced workers gaming the system to provide fast, uniform answers.

## Performance Characteristics
- **Generative Model Inference**: Can resolve 100 LFs over 1M records in < 30 seconds using matrix factorization.
- **Active Learning Latency**: Selection of top-k uncertain samples requires $O(N \log K)$ using max-heaps.

## Research References
- "Snorkel: Rapid Training Data Creation with Weak Supervision" (Ratner et al., VLDB 2017).
- "Active Learning Literature Survey" (Burr Settles, 2009).
- "Computing Krippendorff's Alpha-Reliability" (Hayes & Krippendorff).

## Implementation Notes
Represent the LF output matrix efficiently using Scipy sparse matrices. The Generative Model is implemented as a factor graph trained via Stochastic Gradient Descent.

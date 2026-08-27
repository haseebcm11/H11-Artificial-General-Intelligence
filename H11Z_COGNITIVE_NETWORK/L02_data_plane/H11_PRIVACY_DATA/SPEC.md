> **Layer 2** · Data Plane & Ingestion · `H11-PRIVACY-DATA`

## Purpose

The H11-PRIVACY-DATA agent operates as a rigorous privacy gatekeeper. In an era of expansive web-scraped and user-provided datasets, it is imperative that cognitive training does not inadvertently memorize and leak Personally Identifiable Information (PII) or violate global compliance standards (GDPR, CCPA, HIPAA).

This agent performs deterministic and probabilistic data scrubbing, de-identification, and anonymization on both structured datasets and unstructured text streams. By ensuring bounds on data distinguishability, it enables safe down-stream learning.

## Technical Deep-Dive

H11-PRIVACY-DATA implements a hybrid architecture combining rule-based engines with NLP models (Named Entity Recognition - NER) to detect PII such as names, SSNs, credit cards, and addresses. 

Beyond simple masking, the agent enforces advanced privacy theorems for structured data releases:
1. **k-Anonymity**: Ensures every individual in a dataset is indistinguishable from at least k-1 other individuals with respect to quasi-identifiers (QIs) by applying generalization (e.g., binning ages) and suppression.
2. **l-Diversity**: Extends k-anonymity by ensuring sensitive attributes have at least *l* distinct values within each equivalence class, preventing background knowledge attacks.
3. **t-Closeness**: Requires the distribution of a sensitive attribute in any equivalence class to be close to the distribution of the attribute in the overall table (bounded by threshold *t* using Earth Mover's Distance).
4. **Differential Privacy (Local/Global)**: Injects Laplace or Gaussian noise into numerical queries or feature distributions to provide mathematical guarantees (ε-differential privacy) against membership inference attacks.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| raw_data | Union[String, DataFrame] | Text or structured data containing potential PII |
| context_domain | String | E.g., 'healthcare', 'finance' to tune NER models |
| sensitivity_level | Float | Determines ε for differential privacy and k for k-anonymity |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| sanitized_data | Union[String, DataFrame] | The scrubbed, anonymized dataset |
| privacy_metrics | Dict | Achieved k, l, t values, and ε-loss budget |
| redacted_entities | List[String] | Categories of entities that were removed |

### State Schema
Maintains `PrivacyBudgetTracker` (for tracking differential privacy ε-loss across datasets), and `PseudonymMap` (secure salt-hashed mappings if reversible de-identification is required).

## Dependencies

### Upstream (depends on)
H11-ETL-DATA (provides extracted structured datasets), H11-STREAMING-DATA (unstructured chat/log streams).

### Downstream (feeds into)
H11-FEATURE-STORE, Data Warehouse.

## Failure Modes
1. **NER False Negatives**: A novel entity type evades detection and enters the training corpus.
2. **Privacy Budget Exhaustion**: The ε-limit is reached for a particular dataset, halting further transformations.
3. **Over-Sanitization**: Aggressive k-anonymity generalization strips all predictive utility from the dataset.

## Performance Characteristics
Regex passes are extremely fast (Millions of chars/sec). NER inference is bound by GPU/CPU compute (latency ~20-50ms per document). Generalization algorithms for k-anonymity are computationally intensive (NP-hard optimal k-anonymity), solved via greedy heuristics (Mondrian algorithm) running in O(n log n).

## Research References
- Sweeney, L. (2002). "k-anonymity: A model for protecting privacy."
- Machanavajjhala, A., et al. (2007). "l-diversity: Privacy beyond k-anonymity."
- Dwork, C. (2006). "Differential Privacy."

## Implementation Notes
Use SpaCy or HuggingFace transformers for robust NER. Implement the Mondrian algorithm for multidimensional k-anonymity. Ensure cryptographic hashing uses salted SHA-256 for pseudonymization to prevent rainbow table attacks.

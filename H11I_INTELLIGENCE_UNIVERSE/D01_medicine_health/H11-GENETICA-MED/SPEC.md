> **Layer 1** · Medicine & Health Sciences · `H11-GENETICA-MED`

## Purpose
The H11-GENETICA-MED agent translates raw genomic sequences into actionable medical intelligence. It handles both monogenic Mendelian disorders (variant pathogenicity classification) and complex polygenic diseases (Polygenic Risk Scores, PRS), providing the foundational data for personalized medicine.

## Technical Deep-Dive
For monogenic risk, it computationally implements the American College of Medical Genetics (ACMG) guidelines. It automates criteria evaluation such as population frequency (using gnomAD), in silico consequence prediction (SIFT, PolyPhen, CADD scores), and evolutionary conservation (PhyloP). 
For complex traits, it computes Polygenic Risk Scores (PRS). This involves calculating the weighted sum of risk alleles from a genome-wide association study (GWAS). To handle Linkage Disequilibrium (LD)—where nearby SNPs are highly correlated—it applies LD clumping and thresholding or continuous shrinkage priors (e.g., PRS-CS) to avoid double-counting genomic risk.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `vcf_payload` | `List[str]` | Parsed lines from a Variant Call Format file |
| `hpo_terms` | `List[str]` | Phenotypic manifestations (e.g., HP:0001250 for Seizures) |
| `gwas_summary` | `Dict[str, float]` | Beta weights mapped by dbSNP rsID |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `acmg_results` | `Dict[str, str]` | Variants mapped to Pathogenic, VUS, or Benign |
| `prs_percentile` | `Dict[str, float]` | Patient's risk percentile compared to reference |

### State Schema
Maintains a local caching layer for Linkage Disequilibrium correlation matrices to dramatically speed up PRS calculations without remote database queries.

## Dependencies
### Upstream (depends on)
* None directly within this layer (ingests sequencing pipeline output).
### Downstream (feeds into)
* H11-PHARMACOLOGIA: For pharmacogenomics (e.g., CYP2C19 metabolizer status).
* H11-ONCOLOGIA: For hereditary cancer syndromes (BRCA, Lynch).

## Failure Modes
1. **Ancestry Mismatch:** Applying a PRS developed on European cohorts to an African cohort, leading to wildly inaccurate and potentially harmful risk stratification due to differing LD blocks.
2. **ACMG Over-calling:** Assuming a rare variant is pathogenic simply because it's novel, ignoring structural biology, leading to false-positive disease diagnoses.
3. **Reference Genome Confusion:** Parsing a VCF aligned to GRCh37 with an annotation database built for GRCh38, resulting in entirely mismatched gene disruptions.

## Performance Characteristics
VCF parsing is highly I/O bound. The agent utilizes vectorized operations (e.g., via numpy/pandas equivalents) to apply GWAS beta weights across millions of SNPs in seconds.

## Research References
1. Richards, S., et al. (2015). "Standards and guidelines for the interpretation of sequence variants." *Genetics in Medicine*.
2. Choi, S. W., et al. (2020). "Tutorial: a guide to performing polygenic risk score analyses." *Nature Protocols*.

## Implementation Notes
When scoring ACMG rules, ensure rigorous handling of missing data. An unknown population frequency should not default to 0 (which triggers rare variant pathogenic rules); it must remain 'Unknown' and block certain rule activations.

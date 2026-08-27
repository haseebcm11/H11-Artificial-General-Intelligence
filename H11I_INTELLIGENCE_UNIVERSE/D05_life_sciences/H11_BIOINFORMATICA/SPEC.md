> **Layer 5** · Life Sciences & Biology · `H11-BIOINFORMATICA`

## Purpose
The H11-BIOINFORMATICA agent serves as the general computational backbone for genomic, transcriptomic, and proteomic data processing. It handles large-scale sequence alignments, variant calling, and phylogenetic analyses, bridging raw biological data with actionable insights.

## Technical Deep-Dive
Implements rigorous statistical models for differential expression (e.g., negative binomial distribution for RNA-seq). Utilizes Burrows-Wheeler Transform (BWT) for ultra-fast read alignment and hidden Markov models (HMM) for protein domain identification (Pfam).

## Architecture
- **Input Contract**: FASTQ/FASTA files, raw read counts, or protein sequences.
- **Output Contract**: VCF (Variant Call Format) files, BAM alignments, annotated phylogenetic trees, DE (Differential Expression) matrices.
- **State Schema**: Alignment index caches, transcriptomic abundance matrices, task dependency graphs for pipeline execution.

## Dependencies
- Samtools/BCFtools for SAM/BAM/VCF manipulation.
- DESeq2 / edgeR (via Rpy2 or custom Python ports) for RNA-seq.
- Snakemake or Nextflow for workflow orchestration.

## Failure Modes
- Memory exhaustion during de novo assembly of large genomes (e.g., plant genomes).
- False positives in variant calling due to low coverage or PCR duplicates.
- Reference bias mapping reads to a distant reference genome.

## Performance Characteristics
- Throughput: Can align 100 million paired-end reads in under 30 minutes on a 16-core CPU.
- Scalability: Natively orchestrates cloud-batch jobs for distributed scatter-gather variant calling.

## Research References
- Li H. et al. (BWA, Samtools).
- Genome Analysis Toolkit (GATK) Best Practices.

## Implementation Notes
Core is written in Python, utilizing `pysam` for efficient genomic data access. Pipeline logic uses Directed Acyclic Graphs (DAGs) to parallelize disjoint bioinformatics tasks.

> **Layer 5** · Life Sciences & Biology · `H11-GENEEDITING`

## Purpose
The H11-GENEEDITING agent focuses on designing, scoring, and evaluating precision genetic alterations using programmable nucleases like CRISPR-Cas9, Cas12a, Base Editors, and Prime Editors. It predicts on-target efficacy and off-target risks across whole genomes.

## Technical Deep-Dive
Integrates mechanistic scoring algorithms (e.g., Rule Set 2, CFD score) and deep learning models to predict single guide RNA (sgRNA) activity. It performs thermodynamic modeling of DNA-RNA hybridization and utilizes PAM (Protospacer Adjacent Motif) recognition heuristics. 

## Architecture
- **Input Contract**: Target gene ID or sequence, Cas nuclease variant, target genome, edit type (knockout, knock-in, base edit).
- **Output Contract**: Ranked sgRNA libraries, off-target genomic loci profiles, predicted indel frequency distributions.
- **State Schema**: Nuclease PAM definitions, pre-computed genome indices (e.g., Bowtie/BWA indices for rapid off-target scanning).

## Dependencies
- Bowtie2/BWA for fast short-read (sgRNA) alignment.
- Biopython.
- ViennaRNA for secondary structure prediction of guides.

## Failure Modes
- High off-target cleavage leading to genotoxicity.
- Poor sgRNA loading due to unfavorable secondary RNA structures.
- Low Homology-Directed Repair (HDR) efficiency compared to Non-Homologous End Joining (NHEJ).

## Performance Characteristics
- Off-target scanning: Scans a 3GB genome for mismatches up to 4bp in < 5 seconds using optimized FM-indices.
- Guide generation: Predicts >1000 guides/second.

## Research References
- Doench et al. (Rule Set 2).
- Pinello Lab (CRISPResso2).

## Implementation Notes
Core alignment and off-target enumeration are implemented in optimized C++ binaries invoked via Python subprocesses. Python handles the ML-based efficacy scoring and API routing.

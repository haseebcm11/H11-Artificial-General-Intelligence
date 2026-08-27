> **Layer 5** · Evolutionary Biology & Phylogenetics · `H11-EVOBIO`

## Purpose
The H11-EVOBIO agent reconstructs phylogenetic trees, analyzes sequence alignments, and models evolutionary dynamics such as genetic drift, selection, and speciation.

## Technical Deep-Dive
It utilizes sequence distance matrices to build phylogenies via Neighbor-Joining and UPGMA algorithms. It models evolutionary rates and performs basic substitution model analyses (e.g., Jukes-Cantor).

## Architecture
- **Input Contract**: Biological sequences (DNA/Protein), alignment scores, or mutation rates.
- **Output Contract**: Phylogenetic tree structures, evolutionary distance matrices, and divergence time estimates.
- **State Schema**: Sequence alignments, computed distance matrices, and tree topologies.

## Dependencies
- Biopython (conceptual alignment/tree constructs).

## Failure Modes
- High sequence divergence leading to saturated mutation distances.
- Long branch attraction in simple distance-based tree building.

## Performance Characteristics
Tree building scales $O(N^3)$ for Neighbor-Joining, suitable for hundreds of taxa without parallelization.

## Research References
- Felsenstein, J. (1981). Evolutionary trees from DNA sequences.
- Saitou, N., & Nei, M. (1987). The neighbor-joining method.

## Implementation Notes
Focuses on distance-based tree reconstruction and Wright-Fisher population genetics simulations.

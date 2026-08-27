> **Layer 5** · Zoology & Animal Science · `H11-16`

## Purpose
The Zoologia Agent handles multi-taxonomic modeling of animal kingdoms. It analyzes population dynamics, behavioral ecology, and evolutionary phylogenetics across broad faunal assemblages, providing macroscopic insights into biodiversity, species interactions, and ecosystem services provided by diverse animal populations.

## Technical Deep-Dive
Zoologia leverages Lotka-Volterra equations for predator-prey dynamics, coalescent theory for phylogenetic inference, and spatially explicit individual-based models (IBMs) for animal movement ecology. 

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: Environmental variables, species counts, trait matrices, behavioral observations.
- **Output**: Population trajectory forecasts, interaction webs, extinction risk assessments.
- **State**: Biome topological maps, multi-species interaction matrices.

## Dependencies
- pandas, numpy, scipy
- networkx for interaction webs

## Failure Modes
- Sparse observation data leading to overfitting of population models.
- Unaccounted invasive species destabilizing modeled ecosystems.

## Performance Characteristics
Scales linearly with the number of interacting species `O(N)` for basic matrix models, but `O(N^2)` for full bipartite interaction webs.

## Research References
- Pianka, E. R. (2011). Evolutionary Ecology.
- Krebs, C. J. (2009). Ecology: The Experimental Analysis of Distribution and Abundance.

## Implementation Notes
Focuses on abstracting core traits shared across the metazoan tree of life before specializing.

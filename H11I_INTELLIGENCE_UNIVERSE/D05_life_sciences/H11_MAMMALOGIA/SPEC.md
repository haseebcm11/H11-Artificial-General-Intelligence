> **Layer 5** · Mammalogy & mammals · `H11-MAMMALOGIA`

## Purpose
The H11-MAMMALOGIA agent specializes in mammalian biology, taxonomy, behavior, ecology, and physiology. It handles complex data structures related to mammalian populations, tracking migration patterns, evolutionary lineage, and physiological adaptations.

## Technical Deep-Dive
The agent utilizes a hierarchical taxonomic graph to classify mammalian species, mapping traits, geographical distribution, and phylogenetic relationships. It implements population dynamics models, such as Lotka-Volterra for predator-prey dynamics, and energy balance models for endothermic thermoregulation.

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: Mammalian observation data, physiological metrics, genetic markers.
- **Output**: Phylogenetic trees, population viability analyses, behavioral models.
- **State Schema**: Tracks global mammalian taxa states, population densities, and active ecological models.

## Dependencies
- BioPython (genetics and phylogenetics)
- NetworkX (graphing taxonomic trees)
- NumPy, SciPy (population dynamics modeling)

## Failure Modes
- Taxonomic ambiguity or hybrid species leading to graph cycles.
- Data scarcity for rare or elusive species causing high variance in population models.

## Performance Characteristics
- Fast graph traversal for taxonomic queries (<5ms).
- Dynamic population simulation scales linearly with the number of interacting species.

## Research References
- Vaughan, T. A., Ryan, J. M., & Czaplewski, N. J. (2013). Mammalogy.
- Nowak, R. M. (1999). Walker's Mammals of the World.

## Implementation Notes
Employs an adjacency list for taxonomic graphs. Population models use numerical integration for continuous time simulation.

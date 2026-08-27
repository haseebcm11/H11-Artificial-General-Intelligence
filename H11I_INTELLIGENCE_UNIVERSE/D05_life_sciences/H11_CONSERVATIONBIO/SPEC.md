> **Layer 5** · Conservation biology · `H11-CONSERVATIONBIO`

## Purpose
The H11-CONSERVATIONBIO agent focuses on biodiversity preservation, habitat fragmentation modeling, species reintroduction viability, and resource allocation for conservation efforts. It synthesizes data from other life science agents to inform policy and triage.

## Technical Deep-Dive
Implements metapopulation dynamics (Levins model) to study patch occupancy in fragmented habitats. Uses stochastic dynamic programming for optimal conservation resource allocation. Evaluates landscape connectivity using circuit theory algorithms.

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: GIS habitat maps, threat matrices, budget constraints, species data.
- **Output**: Optimal reserve designs, extinction risk trajectories, connectivity corridors.
- **State Schema**: Patch networks, conservation portfolio, threat levels.

## Dependencies
- NetworkX (landscape connectivity graphs)
- SciPy (optimization, dynamic programming)
- Shapely/Geopandas (spatial operations - implicit representation)

## Failure Modes
- Over-optimizing for a single species, causing cascading failures in others.
- Incorrect parameterization of dispersal probability leading to flawed corridor designs.

## Performance Characteristics
- Circuit theory based connectivity maps are computationally intensive; utilizes sparse matrix solvers.
- Reserve selection (set cover problem) uses fast greedy heuristics.

## Research References
- Primack, R. B. (2014). Essentials of Conservation Biology.
- Moilanen, A., et al. (2009). Spatial Conservation Prioritization.

## Implementation Notes
Marxan-like heuristics implemented for the reserve design problem. Metapopulation state tracks local extinction and colonization rates dynamically.

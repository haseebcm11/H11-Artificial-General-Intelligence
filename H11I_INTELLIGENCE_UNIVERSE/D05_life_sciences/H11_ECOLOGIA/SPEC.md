> **Layer 5** · Ecology & Ecosystems · `H11-ECOLOGIA`

## Purpose
The H11-ECOLOGIA agent analyzes population dynamics, species interactions, and ecosystem energy flows. It helps predict biodiversity changes and ecosystem stability.

## Technical Deep-Dive
Implements Lotka-Volterra predator-prey dynamics and multi-species competition models. Analyzes food web topology, keystone species impacts, and calculates biodiversity indices (Shannon, Simpson).

## Architecture
- **Input Contract**: Species lists, interaction matrices (competition/predation), carrying capacities.
- **Output Contract**: Population time series, stability metrics, biodiversity indices.
- **State Schema**: Current populations, interaction coefficients, environmental carrying capacities.

## Dependencies
- SciPy for solving coupled ODEs.

## Failure Modes
- Unstable interaction matrices causing infinite population growth.
- Extinction of all species due to extreme predation rates.

## Performance Characteristics
Numerical integration scales well for <1000 species. Matrix eigenvalue computations for stability are $O(N^3)$.

## Research References
- May, R. M. (1972). Will a large complex system be stable?
- MacArthur, R. H. (1955). Fluctuations of animal populations and a measure of community stability.

## Implementation Notes
Uses generalized Lotka-Volterra equations. Supports discrete-time stepping for simplicity.

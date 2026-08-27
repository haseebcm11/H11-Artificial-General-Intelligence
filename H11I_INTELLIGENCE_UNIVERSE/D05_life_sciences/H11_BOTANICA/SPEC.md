> **Layer 5** · Botany & Plant Science · `H11-BOTANICA`

## Purpose
The H11-BOTANICA agent models plant growth, photosynthesis, and environmental responses. It simulates morphological development using L-systems and physiological processes using flux models.

## Technical Deep-Dive
Integrates L-system string rewriting for branching topology with a Farquhar-von Caemmerer-Berry (FvCB) model for photosynthesis. It couples light interception and carbon allocation to structural growth.

## Architecture
- **Input Contract**: Environmental parameters (light, CO2, temperature), initial L-system axiom, and production rules.
- **Output Contract**: 3D branch structures, biomass accumulation, photosynthetic rates.
- **State Schema**: Current L-system string, accumulated carbon, and organ mass.

## Dependencies
- Turtle graphics conceptual model for L-system rendering.

## Failure Modes
- Runaway L-system rewriting causing combinatorial explosion in string length.
- Non-physical temperatures causing undefined behavior in kinetic equations.

## Performance Characteristics
L-system expansion grows exponentially; capped at a max depth. Physiological models run in constant time per time step.

## Research References
- Prusinkiewicz, P., & Lindenmayer, A. (1990). The algorithmic beauty of plants.
- Farquhar, G. D., et al. (1980). A biochemical model of photosynthetic CO2 assimilation in leaves of C3 species.

## Implementation Notes
Focuses on parameterized L-system generation and basic biomass-driven rule scaling.

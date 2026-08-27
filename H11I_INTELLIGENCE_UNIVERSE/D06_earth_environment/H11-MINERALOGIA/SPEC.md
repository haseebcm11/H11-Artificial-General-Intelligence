# H11-MINERALOGIA: Mineralogy & Crystals Agent

## Purpose
The H11-MINERALOGIA agent characterizes minerals, their crystallographic structures, and physical properties. It focuses on the classification of naturally occurring solid substances based on their chemical composition and internal structure, facilitating resource exploration and material science integration.

This agent operates within the Earth & Environmental Sciences domain of the H11 Cognitive Substrate, bridging geology with structural chemistry. It evaluates solid solution series, polymorphism, and twinning mechanisms.

## Technical Deep Dive
The architecture utilizes crystallographic databases (e.g., CIF files) and symmetry group algorithms to model unit cells. It applies physical property scaling based on chemical substitutions within crystal lattices.

**Key capabilities:**
- **Crystallographic Modeling**: Calculates lattice parameters, atomic positions, and X-ray diffraction (XRD) patterns for given crystal systems and space groups.
- **Solid Solution Analysis**: Models the variation in physical properties (e.g., refractive index, density) as chemical compositions shift between end-members (e.g., plagioclase feldspars, olivine).
- **Mineral Identification**: Matches observed properties (hardness, cleavage, specific gravity, optical properties) against a comprehensive mineral database to identify unknown samples.

**Architecture Contracts:**
Input JSON must provide structural parameters, chemical formulas, or empirical physical observations. Output JSON delivers synthetic XRD profiles, end-member proportions, or probable mineral identifications with confidence intervals.
Dependencies: Interfaces with H11-PETROLOGIA for rock-forming mineral assemblages.

# H11-PETROLOGIA: Petrology & Rocks Agent

## Purpose
The H11-PETROLOGIA agent is responsible for the study of rocks—igneous, metamorphic, and sedimentary—their origins, occurrence, structure, and history. It provides petrogenetic modeling to understand the conditions of rock formation in the Earth's crust and mantle.

Operating within the Earth & Environmental Sciences domain, this agent interprets geochemical data, phase diagrams, and textural relationships to deduce pressure-temperature-time (P-T-t) paths of geological terrains.

## Technical Deep Dive
The architecture utilizes thermodynamic minimization models (e.g., PERPLE_X, Theriak-Domino inspired algorithms) to calculate stable mineral assemblages for a given bulk rock composition under specified P-T conditions.

**Key capabilities:**
- **Phase Equilibria Modeling**: Generates pseudosections and phase diagrams for multi-component systems (e.g., KFMASH, NCFMASHTO) to determine equilibrium mineral assemblages.
- **Geothermobarometry**: Employs cation exchange and net-transfer reactions between coexisting minerals to estimate the pressure and temperature of rock formation or metamorphism.
- **Magmatic Differentiation**: Models fractional crystallization, partial melting, and assimilation using geochemical mass balance and partition coefficients.

**Architecture Contracts:**
Input JSON must provide bulk rock geochemistry (major and trace elements), assumed P-T conditions, or mineral chemistry data. Output JSON delivers stable mineral modes, P-T estimates, or modeled geochemical trends.
Dependencies: Interfaces with H11-MINERALOGIA for mineral properties and H11-VULCANOLOGIA for magma compositions.

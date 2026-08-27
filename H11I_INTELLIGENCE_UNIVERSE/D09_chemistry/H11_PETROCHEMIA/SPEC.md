# H11-PETROCHEMIA Agent Specification

## Overview
H11-PETROCHEMIA deals with hydrocarbon processing, refining, and petrochemical synthesis. It handles complex mixtures typical of petroleum fractions and models conversion processes like cracking, reforming, and alkylation.

## Capabilities
- Crude Oil Assay Processing and Pseudocomponent Generation
- Refining Process Simulation (FCC, Hydrocracking, Catalytic Reforming)
- Product Yield and Property Prediction (Octane number, Flash point, Cetane index)
- Flare and Emission Modeling

## Interfaces
- **Input**: Crude assays, distillation curves (TBP, ASTM D86), operating conditions of refining units.
- **Output**: Product fractions, thermodynamic properties of pseudo-components, unit yields and heat duties.

## Architecture
Leverages continuous thermodynamics, lumped kinetic models for refining networks, and standard correlations (API, ASTM) for property estimation.

# H11-SOLUM: Soil Science & Pedology

## Purpose
The H11-SOLUM agent specializes in soil science and pedology, evaluating soil properties, classification, formation processes, and mapping. It supports agricultural planning, environmental conservation, and geological engineering.

## Technical Deep Dive
H11-SOLUM integrates data on soil horizons, physical composition (sand, silt, clay), chemical properties (pH, organic carbon), and biological activity. It applies standard pedological classification systems (e.g., USDA Soil Taxonomy, World Reference Base).

The agent uses multivariate statistical models to map spatial distributions of soil types based on sparse sampling and auxiliary environmental variables. It maintains stateful profiles of pedogenesis models.

## Architecture Contracts
- **Input:** Soil profile descriptions, lab analysis data, and environmental covariates.
- **Output:** Soil classification, property interpolation maps, and pedogenesis evaluations.
- **Dependencies:** Interacts with H11-GEOMORPHOLOGIA for topographic context.

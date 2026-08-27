> **Layer 5** · Herpetology & Reptiles/Amphibians · `H11-19`

## Purpose
The Herpetologia Agent focuses on ectothermic physiological modeling, environmental toxigenomics (especially for amphibians), and venom proteomics. It provides vital metrics on climate change susceptibility based on ectotherm thermal regulatory limits.

## Technical Deep-Dive
Utilizes biophysical heat-transfer equations to model operative environmental temperatures (Te) for microhabitats. Employs compartment models for toxicological accumulation (e.g., Batrachochytrium dendrobatidis spread in frog populations).

## Architecture (Input Contract, Output Contract, State Schema)
- **Input**: High-res terrain models, solar radiation data, venom protein sequences.
- **Output**: Thermal suitability maps, disease transmission rates, venom molecular binding affinities.
- **State**: Operative temperature grids, amphibian population health statuses.

## Dependencies
- numpy, scipy, biopython
- rasterio for terrain/solar mapping

## Failure Modes
- Coarse terrain maps lead to missing vital micro-refugia (like under-rock shaded areas) causing false extinction predictions.
- Over-generalizing water loss rates across different amphibian skin structures.

## Performance Characteristics
High spatial resolution thermal mapping is memory intensive. Requires tiling `O(W * H)` grids.

## Research References
- Pough, F. H., et al. (2015). Herpetology.
- Kearney, M., & Porter, W. (2009). Mechanistic niche modelling: combining physiological and spatial data to predict species' ranges.

## Implementation Notes
Microhabitat modeling handles the solar, longwave, convective, and conductive heat exchanges specific to ground-dwelling ectotherms.

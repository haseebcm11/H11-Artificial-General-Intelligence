# H11-PALEONTOLOGIA: Paleontology & Fossils Agent

## Purpose
The H11-PALEONTOLOGIA agent serves to systematically catalog, analyze, and interpret fossil records to understand evolutionary biology, ancient ecosystems, and the geological timeline. It aids in the reconstruction of paleoenvironments and the phylogenetic relationships between extinct organisms.

This agent operates within the H11 Earth & Environmental Sciences domain. It provides tools for taphonomic analysis, morphological trait classification, and stratigraphic correlation using index fossils.

## Technical Deep Dive
The architecture relies on morphological feature extraction, cladistic analysis algorithms, and spatiotemporal fossil occurrence databases. It uses statistical models to infer paleodiversity, extinction rates, and evolutionary trends over deep time.

**Key capabilities:**
- **Cladistic Analysis**: Constructs phylogenetic trees (cladograms) based on a matrix of morphological or inferred genetic traits using maximum parsimony and maximum likelihood methods.
- **Paleoecology Reconstruction**: Infers ancient environmental conditions (e.g., temperature, depth, salinity) by analyzing fossil assemblages and functional morphology.
- **Biostratigraphy**: Correlates sedimentary rock layers across different geographic regions using the temporal ranges of index fossils.

**Architecture Contracts:**
Input JSON must contain fossil specimen data, morphological matrices, or stratigraphic layer descriptions. Output JSON provides phylogenetic trees (Newick format), paleodiversity metrics, or paleoenvironmental inferences.
Dependencies: Interfaces with H11-SEDIMENTOLOGIA for stratigraphic context and H11-BIOLOGIA (if present) for comparative anatomy with extant species.

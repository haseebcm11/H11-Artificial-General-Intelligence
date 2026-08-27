> **Layer 1** · Medicine & Health Sciences · `H11-IMMUNOLOGIA`

## Purpose
H11-IMMUNOLOGIA simulates the complex dynamics of the human immune system, differentiating self from non-self. It models both the rapid, non-specific innate immune response and the highly specific, memory-driven adaptive immune response. It serves as the primary defense mechanism simulator against pathogens identified by VIROLOGIA, BACTERIOLOGIA, and MYCOLOGIA.

## Technical Deep-Dive
The agent employs a multi-agent particle simulation for cellular interactions and reaction-diffusion equations for cytokine gradients. Phagocytes (macrophages, neutrophils) use chemotaxis algorithms to follow inflammatory chemokine gradients. 

The adaptive immune response uses shape-space matching (a mathematical abstraction of epitope-paratope affinity) to model T-cell receptor and B-cell antibody specificity. The Clonal Selection Theory is modeled via genetic algorithms, where high-affinity clones proliferate, mutate, and undergo affinity maturation. It tracks MHC Class I and II presentation pathways to accurately model T-cell activation.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| antigen_profile | AntigenData | The molecular signature of an invading pathogen or tumor cell. |
| site_of_infection | LocationID | Anatomical location from ANATOMIA. |
| local_cytokines | CytokineProfile | Current inflammatory milieu. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| immune_response | ResponseVector | Type and strength of response (e.g., Th1, Th2, CD8+ cytotoxic). |
| memory_generated | ImmuneMemory | New T/B cell clones added to the repertoire. |

### State Schema
Maintains an `ImmuneRepertoire` dictionary mapping shapes/epitopes to clonal frequencies, and a `SystemicInflammation` index.

## Dependencies
### Upstream (depends on)
H11-PATHOLOGIA (cell death signals), Pathogen Agents (antigen inputs)
### Downstream (feeds into)
H11-PHYSIOLOGIA (fever, systemic shock), H11-CLINICA

## Failure Modes
1. Autoimmune Cross-Reactivity: Epitope matching threshold set too loose, causing self-tissue attack.
2. Cytokine Storm Runaway: Positive feedback loop between macrophages and T-cells without Treg suppression.
3. Repertoire Exhaustion: Exhaustion of T-cells during simulated chronic infection models.

## Performance Characteristics
High memory footprint for tracking thousands of unique clonal populations. Chemotaxis spatial simulation requires optimized KD-trees for cellular neighborhood lookups.

## Research References
- Janeway's Immunobiology (Effector mechanisms).
- Perelson's mathematical models of immune response.

## Implementation Notes
Implemented with a localized cellular automaton for tissue-level interactions and global ODEs for lymph node clonal expansion.

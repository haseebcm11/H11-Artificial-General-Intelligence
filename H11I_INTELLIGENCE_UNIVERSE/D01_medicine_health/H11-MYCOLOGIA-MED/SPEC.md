> **Layer 1** · Medicine & Health Sciences · `H11-MYCOLOGIA-MED`

## Purpose
H11-MYCOLOGIA-MED models human fungal infections, ranging from superficial dermatophytes (ringworm, tinea) to severe systemic mycoses (histoplasmosis, invasive aspergillosis). Fungi, being eukaryotes, present unique modeling challenges regarding drug targeting and immune evasion. This agent maps the slow, insidious progression characteristic of fungal pathogens.

## Technical Deep-Dive
The agent utilizes a dimorphic phase-transition engine. Many pathogenic fungi exist as molds in the environment and yeasts in the human body; the agent dynamically shifts their morphological state based on simulated temperature and CO2 concentrations provided by PHYSIOLOGIA.

Growth is modeled spatially via hyphal extension algorithms (a form of diffusion-limited aggregation) and spore dissemination. Immune evasion tactics, such as polysaccharide capsule shedding (e.g., *Cryptococcus*), are modeled as stealth vectors that suppress the local chemotaxis signals consumed by IMMUNOLOGIA.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| fungal_strain | FungalSpecies | Taxonomic definition, dimorphic capability, virulence factors. |
| host_immunity_state | ImmuneStatus | Competent, immunocompromised, neutropenic. |
| environmental_temp | Float | Local tissue temperature. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| fungal_burden | Float | Mass of fungal growth. |
| tissue_invasion_depth | Float | Spatial penetration of hyphae. |
| morphological_form | FungalForm | Yeast, Mold, or Spherule. |

### State Schema
Tracks `FungalColonies` mapping spatial coordinates to hyphal density or yeast cell counts. Maintains a global `DimorphismState`.

## Dependencies
### Upstream (depends on)
H11-PHYSIOLOGIA (temp/CO2), H11-IMMUNOLOGIA (immune status)
### Downstream (feeds into)
H11-PATHOLOGIA (granuloma formation, necrosis)

## Failure Modes
1. Premature Dimorphism: Triggering yeast-to-mold transition incorrectly in deep tissue, invalidating pathogenesis logic.
2. Runaway Hyphal Growth: Geometric expansion of hyphae exceeding anatomical bounds (e.g., growing through bone without osteoclast activity).
3. Evasion Overpower: Capsule shedding totally blinding IMMUNOLOGIA, preventing any clearance even in healthy hosts.

## Performance Characteristics
Low CPU overhead due to the slow growth rate of fungi compared to bacteria/viruses. Spatial expansion calculations are updated infrequently (e.g., daily ticks).

## Research References
- Medical Mycology textbook (Kwon-Chung).
- Modeling thermal dimorphism in pathogenic fungi.

## Implementation Notes
Fungal growth is calculated on a much longer timescale (days/weeks) compared to VIROLOGIA/BACTERIOLOGIA. Focus is on chronic inflammation and granuloma formation.

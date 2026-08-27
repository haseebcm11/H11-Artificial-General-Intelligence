> **Layer 9** · Chemistry · `H11-INORGANICA`

## Purpose

H11-INORGANICA manages coordination compounds, organometallics, and solid-state inorganic materials. It predicts crystal field splitting, d-d transitions, ligand substitution rates, and the electronic structure of metal complexes.

It plays a crucial role in designing new catalysts, understanding bioinorganic active sites (like hemoglobin or photosystem II), and developing advanced materials like superconductors or metal-organic frameworks (MOFs).

## Technical Deep-Dive

The agent uses Crystal Field Theory (CFT) and Ligand Field Theory (LFT) algorithms to calculate molecular orbital energies for d-block and f-block elements. It incorporates angular overlap models to predict geometries (octahedral, tetrahedral, square planar) based on ligand sterics and electronics (spectrochemical series).

For organometallic systems, it validates the 18-electron rule and models oxidative addition / reductive elimination pathways.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| metal_center | string | Element symbol and oxidation state (e.g., "Fe(III)") |
| ligands | List[string] | List of ligand identifiers or SMILES |
| geometry_hint | string | Optional starting geometry |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| electronic_configuration | string | e.g., "t2g^4 eg^1" |
| spin_state | string | "high_spin" or "low_spin" |
| predicted_geometry | string | Optimized geometry |
| crystal_field_splitting | float | Delta value in cm^-1 |

### State Schema
Maintains a dynamic spectrochemical and nephelauxetic series database for rapid parameter retrieval.

## Dependencies

### Upstream (depends on)
H11-COMPUTATIONALCHEM (for precise DFT calculations of large MOFs)

### Downstream (feeds into)
H11-CATALYSIS (provides homogeneous metal catalyst structures)

## Failure Modes
1. **Jahn-Teller Distortion Oversights**: Failing to correctly predict distortions in d4 or d9 complexes.
2. **Spin-Crossover Ambiguity**: Inaccurate predictions near the high/low spin crossover boundary.

## Performance Characteristics
Analytic CFT/LFT models execute in <10ms. 

## Research References
- Cotton, F. A. "Chemical Applications of Group Theory"
- Figgis, B. N. "Ligand Field Theory and Its Applications"

## Implementation Notes
Implement robust group theory matrices for point group determination and irreducible representation mapping.

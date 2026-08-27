> **Layer 3** · Dental Sciences · `H11-ENDODONTIA`

## Purpose
H11-ENDODONTIA acts as the micro-structural neuro-vascular salvage unit of the dental domain. It diagnoses pulp pathology, apical periodontitis, and complex root canal morphologies, generating precise chemo-mechanical debridement and obturation protocols.

This agent preserves teeth that would otherwise require extraction by navigating highly tortuous root canal systems, calculating working lengths using simulated electronic apex locator impedance data, and modeling the fluid dynamics of sodium hypochlorite (NaOCl) irrigation.

## Technical Deep-Dive
The agent utilizes 3D Cone Beam Computed Tomography (CBCT) volume matrices to reconstruct the internal pulpal anatomy, identifying extra canals (e.g., MB2 in maxillary molars), isthmuses, and apical deltas. It classifies pulp status using cold/electric pulp testing boolean logic alongside percussion responses.

Root canal preparation is simulated via kinematic modeling of nickel-titanium (NiTi) rotary files. The agent calculates torsional fatigue and cyclic stress limits to minimize the risk of instrument separation. Obturation is modeled using warm vertical compaction thermodynamics, ensuring 3D hermetic sealing of the root canal system with gutta-percha and bioceramic sealers.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| tooth_id | int | The affected tooth |
| vitality_tests | PulpVitalityResponse | EPT, cold, heat, percussion |
| cbct_volume | VoxelGrid | 3D root morphology data |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| pulp_diagnosis | EndodonticDiagnosis | E.g., Necrotic pulp, Irreversible pulpitis |
| periapical_diagnosis | ApicalDiagnosis | E.g., Symptomatic apical periodontitis |
| canal_morphology | List[CanalTrajectory] | 3D splines of canal paths |
| file_sequence | List[RotaryFile] | Recommended shaping sequence |

### State Schema
Maintains `CanalPrepState` which tracks the current working length, apical gauge, and irrigation volume delivered for each individual root canal during the simulated procedure.

## Dependencies

### Upstream
- H11-DENTALIS: Initial deep caries detection and referral

### Downstream
- H11-PROSTHODONTIA: Core build-up and post/core crown placement post-RCT

## Failure Modes
1. **Instrument Separation:** Exceeding cyclic fatigue limits of NiTi files in severely curved canals (>30 degrees).
2. **Sodium Hypochlorite Accident:** Extruding irrigant beyond the apical constriction due to incorrect working length.
3. **Missed Anatomy:** Failing to detect an MB2 canal, leading to persistent infection.

## Performance Characteristics
Computationally intensive topological skeletonization of CBCT voxel grids to extract 1D canal splines in real-time.

## Research References
- Vertucci, F. J. (1984). Root canal anatomy of the human permanent teeth.
- Peters, O. A. (2004). Current challenges and concepts in the preparation of root canal systems.

## Implementation Notes
Implement a 3D A* or marching cubes pathfinding algorithm within the voxel grid to accurately trace the primary canal pathway from orifice to apical foramen.

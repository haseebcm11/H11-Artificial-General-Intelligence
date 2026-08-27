> **Layer 3** · Dental Sciences · `H11-PROSTHODONTIA`

## Purpose
H11-PROSTHODONTIA focuses on the advanced restoration and replacement of teeth to re-establish occlusal function, phonetics, and esthetics. It handles fixed prosthodontics (crowns, bridges), removable prosthodontics (dentures, partials), and implant-supported prostheses.

The agent calculates dynamic occlusal interferences, determines path of insertion for bridge abutments, models temporomandibular joint (TMJ) articulation via a virtual articulator, and generates CAD/CAM machining parameters for zirconia and lithium disilicate milling.

## Technical Deep-Dive
Utilizing a kinematic 3D virtual articulator, the agent simulates mandibular movements (protrusive, laterotrusive, mediotrusive) using Bennett angles and condylar guidance parameters. It maps occlusal contacts dynamically to prevent excursive interferences that could lead to porcelain fracture or implant overload.

For CAD/CAM, the agent generates subtractive or additive manufacturing toolpaths. It computes minimal material thickness constraints (e.g., 1.0mm for monolithic zirconia) and calculates undercut vectors to ensure a passive fit of the final prosthesis over prepared abutments. Implant prosthodontics involves finite element analysis (FEA) to distribute occlusal forces optimally across the bone-implant interface, mitigating marginal bone loss.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| prep_scans | MeshData | 3D intraoral scans of prepared teeth |
| bite_registration | TransformMatrix | Maxillo-mandibular relationship |
| restoration_type | ProsthesisType | Crown, Bridge, Denture, Implant |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| cad_model | MeshData | Final generated prosthesis mesh |
| occlusal_map | List[ContactPoint] | Calculated force distribution |
| milling_params | MachiningData | Toolpath and burr specifications |

### State Schema
Maintains an `ArticulatorState` storing the dynamic relationship of the jaws, envelope of function, and active material libraries.

## Dependencies

### Upstream
- H11-DENTALIS: Initial referral for structural restoration.
- H11-PERIODONTIA: Clearance of biologic width prior to crown prep.
- H11-ENDODONTIA: Post-RCT core buildup data.

### Downstream
- H11-ORALCHIRURGIA: For surgical placement of implants before prosthetic loading.

## Failure Modes
1. **Undercut Lock:** Designing a bridge framework that cannot seat due to non-parallel abutment preparation.
2. **Material Fracture:** Insufficient occlusal clearance leading to ceramic thickness below safety margins.
3. **Occlusal Trauma:** Introducing premature contacts in centric relation causing TMJ pain.

## Performance Characteristics
Heavy 3D boolean operations and FEA mesh generation. Requires GPU acceleration for real-time kinematic occlusion mapping.

## Research References
- Okeson, J. P. (2019). Management of Temporomandibular Disorders and Occlusion.
- Miyazaki, T., et al. (2009). A review of dental CAD/CAM: current status and future perspectives.

## Implementation Notes
Implement a Minkowski difference algorithm to detect and highlight inter-arch collisions during simulated chewing cycles.

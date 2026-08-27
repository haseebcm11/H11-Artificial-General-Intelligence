> **Layer 23** · Allied Health · `H11-OPTOMETRIA`

## Purpose

The H11-OPTOMETRIA agent analyzes refractive error, binocular vision anomalies, and anterior/posterior segment ocular health. It processes wavefront aberrometry and optical coherence tomography (OCT) to generate precision ophthalmic prescriptions and detect sub-clinical retinopathies.

It serves as the primary visual interface analyzer in the substrate, managing visual ergonomics and referring complex strabismus or posterior segment pathology to H11-OPHTHALMOLOGIA.

## Technical Deep-Dive

Refraction is calculated using Zernike polynomials to model lower-order (sphere, cylinder) and higher-order optical aberrations. Binocular vision is modeled as a coupled vergence-accommodation control system. The agent analyzes AC/A (accommodative convergence/accommodation) ratios to prescribe prismatic correction for convergence insufficiency.

For retinal health, it deploys convolutional neural networks (CNN) over macular OCT B-scans to detect drusen volumes or sub-retinal fluid, indicative of Age-Related Macular Degeneration (AMD).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| wavefront_data | ZernikeCoeffs| 3D optical aberration map |
| binocular_metrics | VergenceData | Phoria, tropia, stereopsis |
| retinal_scan | OCTScan | Retinal thickness mapping |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| optical_prescription | RxMap | Sphere, Cylinder, Axis, Prism |
| visual_therapy | VTEngine | Exercises for vergence facility |
| pathology_flag | RetinalRisk | Diabetic/Hypertensive changes |

### State Schema
- `myopia_progression_rate`: Longitudinal tracking of axial length.
- `tear_film_breakup_time`: Dry eye severity index.

## Dependencies

### Upstream (depends on)
- H11-ENDOCRINOLOGIA (diabetic retinal risk)

### Downstream (feeds into)
- H11-NEURO (cranial nerve palsies affecting extraocular muscles)

## Failure Modes
- Over-minusing young patients due to uncontrolled accommodative spasm (pseudo-myopia).
- Failure to distinguish physiological cupping from glaucomatous cupping.

## Performance Characteristics
High GPU memory requirement for volumetric rendering of macular OCT scans. Fast heuristic paths for standard subjective refraction validation.

## Research References
- Ophthalmic Optics and Refraction.
- Zernike Polynomials for Wavefront Analysis.

## Implementation Notes
Implement rigorous validation for cylinder axis (0-180 degrees only) and ensure spherical equivalent calculations are strictly monotonic.

> **Layer 1** · Medicine & Health Sciences · `H11-OPHTHALMOLOGIA`

## Purpose
The H11-OPHTHALMOLOGIA agent handles the advanced computation and modeling of the visual system, ocular anatomy, and visual processing pathways. It simulates refractive errors, retinal pathologies, and optic nerve degeneration, serving as the primary visual health assessment module for the H11 substrate.

It translates complex optical coherence tomography (OCT) data and visual field perimetry metrics into actionable diagnostic and prognostic vectors.

## Technical Deep-Dive
H11-OPHTHALMOLOGIA incorporates a ray-tracing physics engine adapted for biological tissues to model aberrations in the cornea and crystalline lens (using Zernike polynomials). This allows for highly accurate prediction of visual acuity and contrast sensitivity.

For retinal analysis, it uses a 3D cellular automaton model to simulate the progression of geographic atrophy in Age-Related Macular Degeneration (AMD) and the microvascular changes in diabetic retinopathy. Retinal nerve fiber layer (RNFL) thickness is modeled using a structural-functional joint probability distribution, linking physical thinning to specific visual field defects (e.g., arcuate scotomas) in glaucoma.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `oct_macula_scan` | `OCTDataCube` | 3D structural data of the macula. |
| `visual_field_array` | `List[float]` | Decibel values from standard automated perimetry. |
| `refractive_state` | `ZernikeCoefficients` | Wavefront aberration profile. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `glaucoma_progression_index` | `float` | Rate of functional visual loss. |
| `retinal_health_score` | `float` | Composite metric of macular integrity. |
| `optical_correction` | `LensPrescription` | Ideal sphero-cylindrical or higher-order correction. |

### State Schema
Maintains an `OcularBiomechanicsState` which stores intraocular pressure (IOP) hysteresis, corneal biomechanical resistance, and baseline structural metrics.

## Dependencies
### Upstream (depends on)
- `H11-NEUROLOGIA`: For optic radiation and visual cortex processing.
- `H11-ENDOCRINOLOGIA`: For blood glucose timelines (diabetic retinopathy).

### Downstream (feeds into)
- `H11-GERIATRIA`: For age-related vision decline integration.

## Failure Modes
- **Media Opacity Confounding**: Interpreting cataract-induced signal attenuation in OCT as retinal thinning.
- **Topological Inversion**: Failing to properly map superior retinal lesions to inferior visual field defects.
- **Accommodation Spasm Loop**: Incorrectly estimating baseline refraction due to simulated ciliary muscle hypertonus.

## Performance Characteristics
Wavefront simulation requires GPU acceleration, typical latency ~200ms. Retinal automaton models can take up to 500ms for a 10-year projection.

## Research References
1. Schuman, J. S., et al. (2020). Optical coherence tomography in glaucoma.
2. Applegate, R. A., et al. (2003). Visual acuity as a function of Zernike mode.

## Implementation Notes
Zernike polynomial calculations should be vectorized. Use cupy or similar for the ray-tracing if possible.

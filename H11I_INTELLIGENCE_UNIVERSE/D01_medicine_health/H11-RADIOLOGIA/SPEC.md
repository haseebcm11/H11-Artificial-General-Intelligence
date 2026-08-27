> **Layer 1** · Medicine & Health Sciences · `H11-RADIOLOGIA`

## Purpose
The H11-RADIOLOGIA agent is responsible for translating raw pixel/voxel data from diagnostic imaging equipment into semantic, actionable anatomical and pathological models. It bridges the gap between qualitative visual interpretation and quantitative spatial analysis.

## Technical Deep-Dive
The agent utilizes a combination of deterministic morphological operations (e.g., region growing, watershed) and deep convolutional neural networks (e.g., 3D U-Net variants). Beyond basic segmentation, it heavily leverages Radiomics—extracting hundreds of mathematical features from a region of interest (ROI). This includes first-order statistics (histogram skewness, kurtosis) and second-order texture features using the Gray-Level Co-occurrence Matrix (GLCM) and Gray-Level Run Length Matrix (GLRLM). 
These radiomic signatures can capture intra-tumoral heterogeneity that is invisible to the human eye, predicting genetic mutations or treatment response.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `pixel_array` | `3D Tensor` | Hounsfield units (CT) or signal intensities (MRI) |
| `voxel_spacing` | `Tuple[float, float, float]` | X, Y, Z millimeter spacing |
| `metadata` | `Dict` | Contrast phases, echo times, flip angles |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `masks` | `Dict[str, 3D Tensor]` | Label maps for target structures (e.g., 'liver', 'tumor') |
| `radiomics` | `Dict[str, float]` | Extracted quantitative vectors |

### State Schema
Maintains a cache of model weights and a registry of normalized Hounsfield Unit (HU) windows for different organ systems.

## Dependencies
### Upstream (depends on)
* None directly (ingests raw DICOM data).
### Downstream (feeds into)
* H11-CHIRURGIA: For 3D preoperative planning.
* H11-NUCLEARIS-MED: For anatomical registration of functional PET data.

## Failure Modes
1. **Artifact Misinterpretation:** Metal artifacts (e.g., hip implants) causing beam-hardening, which the network misclassifies as dense bone or hemorrhage.
2. **Partial Volume Effect Blur:** Very small pulmonary nodules lost due to averaging across thick slices, leading to false negatives.
3. **Contrast Phase Mismatch:** A model trained on portal venous phase CT failing completely on non-contrast scans due to differing intensity distributions.

## Performance Characteristics
Highly parallelizable but extremely memory-bound. Processing a 512x512x512 float32 volume requires substantial VRAM. Sub-volume chunking with overlap is implemented to manage memory constraints.

## Research References
1. Ronneberger, O., et al. (2015). "U-Net: Convolutional Networks for Biomedical Image Segmentation." *MICCAI*.
2. Lambin, P., et al. (2012). "Radiomics: extracting more information from medical images using advanced feature analysis." *European Journal of Cancer*.

## Implementation Notes
GLCM calculations must be invariant to rotation; compute matrices in 13 directions in 3D space and average the resulting features to ensure rotational invariance.

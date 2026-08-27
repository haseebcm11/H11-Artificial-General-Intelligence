> **Layer 19** · Arts, Design & Creativity · `H11-PHOTOGRAPHIA`

## Purpose

The H11-PHOTOGRAPHIA agent models the physical processes of cameras. From thick-lens optics arrays to photon-shot noise on a CMOS sensor, it transforms absolute radiance maps into photographically realistic images.

## Technical Deep-Dive

Utilizes ray-tracing specifically designed for complex lens assemblies (modeling elements, groups, and glass refractive indices like Abbe numbers) to simulate exact depth of field, optical vignetting (cat's eye bokeh), and chromatic aberrations. The sensor model incorporates Poisson distributions for shot noise and Gaussian distributions for read/thermal noise.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| scene_radiance_map | bytes | EXR/HDR light map |
| focal_length_mm | float | Lens focal length |
| aperture_f_stop | float | Aperture size |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| raw_image_data | bytes | Bayer pattern data |
| noise_profile | Dict | Noise characterization |

### State Schema
- `sensor_temperature_c`: Rises during long exposures, increasing thermal noise.

## Dependencies

### Upstream (depends on)
- H11-RAYTRACER (Layer 18): Provides the initial light transport map.

### Downstream (feeds into)
- H11-CINEMATOGRA: Feeds frames into sequence processing.

## Failure Modes
- Infinite loop in lens flare caustic scattering.
- Buffer overflow when shooting continuous bursts.

## Performance Characteristics
Highly parallelizable for pixel-level sensor simulation. Demosaicing requires tensor cores for modern neural-network based approaches.

## Research References
- Real-Time Lens Flare Rendering.
- A Physically-Based Camera Model for Computer Graphics.

## Implementation Notes
Implement the demosaicing algorithm using a lightweight CNN for best results, falling back to AHD (Adaptive Homogeneity-Directed) for fast previews.

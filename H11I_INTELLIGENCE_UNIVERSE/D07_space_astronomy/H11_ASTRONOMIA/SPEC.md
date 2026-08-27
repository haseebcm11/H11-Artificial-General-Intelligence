> **Layer 7** · Space & Astronomy · `H11-ASTRONOMIA`

## Purpose

The H11-ASTRONOMIA agent manages observational astronomy data processing, coordinating telescope arrays, and interpreting sky surveys. It processes raw astrometric, photometric, and spectroscopic data to identify and track celestial objects.

This agent acts as the primary sensory interpreter for the space domain, converting raw photons into structured catalogs of stars, galaxies, and transients.

## Technical Deep-Dive

ASTRONOMIA implements advanced coordinate transformations (ICRS, J2000, Galactic) and utilizes proper motion vectors combined with parallax to establish 3D spatial models of the local stellar neighborhood.

It heavily relies on point-spread function (PSF) fitting for dense star fields and utilizes Lomb-Scargle periodograms for detecting periodic variability in light curves.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| observation_id | str | Unique ID for the observation batch |
| raw_lightcurve | List[float] | Time-series photometric data |
| coordinate_system | str | ICRS, Galactic, Ecliptic |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| classified_objects | List[dict] | Catalog of identified objects |
| astrometric_solution | dict | Proper motion and parallax |

### State Schema
Maintains a local catalog cache of recently observed objects and current telescope pointing states.

## Dependencies

### Upstream (depends on)
H11-SENSOR (for raw CCD feeds)

### Downstream (feeds into)
H11-ASTROPHYSICA, H11-PLANETOLOGIA

## Failure Modes
- PSF Fitting Non-convergence
- Coordinate Transformation Singularities
- Zero-point Calibration Drift

## Performance Characteristics
High throughput data pipeline, requiring GPU acceleration for bulk PSF fitting. Latency < 50ms for transient alerts.

## Research References
- Gaia Mission Astrometry Standards
- LSST/Rubin Observatory Data Management Design
- SDSS Photometric Calibration

## Implementation Notes
Use ASTROPY for underlying coordinate transformations to ensure precision.

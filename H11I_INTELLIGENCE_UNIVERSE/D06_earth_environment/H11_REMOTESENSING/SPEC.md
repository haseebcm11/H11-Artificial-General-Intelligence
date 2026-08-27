# H11-REMOTESENSING: Remote Sensing & Satellite Imagery

## Purpose
The H11-REMOTESENSING agent processes, analyzes, and interprets data acquired by sensors that are not in physical contact with the object being observed, primarily focusing on satellite and aerial imagery.

## Technical Deep Dive
H11-REMOTESENSING handles multi-spectral, hyperspectral, and Synthetic Aperture Radar (SAR) data. It implements radiometric calibration, atmospheric correction, and orthorectification pipelines.

The agent provides capabilities for image classification (supervised and unsupervised), spectral index calculation (NDVI, EVI, NDWI), change detection over time-series data, and feature extraction. It utilizes machine learning models tailored for earth observation data cubes.

## Architecture Contracts
- **Input:** Raw or pre-processed satellite imagery formats (GeoTIFF, NetCDF, HDF5), spectral band definitions.
- **Output:** Classified maps, extracted features, spectral index layers, time-series anomaly reports.
- **Dependencies:** Feeds raster products to H11-GIS and H11-CARTOGRAPHIA.

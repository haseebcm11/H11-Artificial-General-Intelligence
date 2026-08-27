# H11-VULCANOLOGIA: Volcanology Agent

## Purpose
The H11-VULCANOLOGIA agent is dedicated to the study of volcanoes, lava, magma, and related geological, geophysical, and geochemical phenomena. It is designed to model volcanic eruptions, forecast volcanic hazards, and analyze the composition and rheology of volcanic products.

This agent operates within the H11 Cognitive Substrate's Earth & Environmental Sciences domain. It provides quantitative risk assessment models, supports real-time monitoring data ingestion (e.g., seismic swarms, gas emissions, ground deformation), and generates simulation outputs for ash dispersion and lava flow trajectories.

## Technical Deep Dive
The architecture integrates fluid dynamics for magma ascent and lava flow modeling, thermodynamics for phase changes during ascent, and probabilistic frameworks for hazard assessment. The agent leverages Bayesian networks to synthesize multi-parametric monitoring data (seismic, geodetic, geochemical) into coherent alert levels and eruption probabilities.

**Key capabilities:**
- **Magma Rheology Simulation**: Calculates viscosity and yield strength as functions of temperature, composition, and crystal/bubble content.
- **Plume Dynamics**: Simulates the buoyant ascent of volcanic plumes, incorporating air entrainment, particle aggregation, and atmospheric wind fields to predict ashfall distribution.
- **Hazard Zonation**: Produces spatial probability maps for various volcanic hazards including pyroclastic density currents (PDCs), lahars, and lava flows using Monte Carlo simulations.

**Architecture Contracts:**
Input JSON must provide volcanic system parameters, monitoring time-series, or specific scenario definitions. Output JSON delivers hazard probabilities, simulation grids (GeoJSON format), or rheological profiles.
Dependencies: Interfaces with H11-PETROLOGIA for magma composition and H11-METEOROLOGIA for ash dispersion wind data.

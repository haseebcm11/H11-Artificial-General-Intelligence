# H11-CRYSTALLOGRAPHIA Agent Specification

## Overview
H11-CRYSTALLOGRAPHIA is an agent for solid-state chemistry, crystal structure prediction, and materials informatics. It analyzes atomic arrangements, unit cell parameters, and electronic band structures of crystalline materials.

## Capabilities
- Bravais Lattice and Space Group Identification
- X-Ray Diffraction (XRD) Pattern Simulation
- Crystal Structure Relaxation and Defect Analysis
- Band Gap and Density of States (DOS) Estimation
- Mechanical Moduli (Bulk, Shear, Young's) for Crystals

## Interfaces
- **Input**: Crystal structures (CIF, POSCAR), elemental composition, external pressure/temperature.
- **Output**: Space group, XRD patterns, band structures, thermodynamic stability (formation energy).

## Architecture
Combines crystallographic symmetry engines (like spglib), empirical interatomic potentials, and interfaces with Density Functional Theory (DFT) databases (e.g., Materials Project) for structural analysis.

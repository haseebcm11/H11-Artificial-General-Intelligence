> **Layer 2** · Telecommunications · `H11-FIBER`

## Purpose

The H11-FIBER agent focuses on the physical and link layer properties of fiber optic networks. It models optical signal propagation, multiplexing (WDM/DWDM), dispersion, and attenuation over single-mode and multi-mode fibers. 

## Technical Deep-Dive

It employs non-linear Schrödinger equations to model signal distortion in optical fibers over long distances. It also manages the state of optical amplifiers (EDFAs) and dispersion compensation modules along paths.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| wavelength_nm | float | Carrier wavelength |
| launch_power_dbm | float | Input optical power |
| distance_km | float | Fiber length |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| received_power_dbm | float | Received optical power |
| osnr_db | float | Optical Signal-to-Noise Ratio |

### State Schema
Optical topology graph with edge attributes containing fiber characteristics (chromatic dispersion, PMD, attenuation coefficients).

## Dependencies
- Upstream: None
- Downstream: H11-NETWORKING

## Failure Modes
- Fiber cuts (total signal loss)
- Component aging increasing attenuation

## Performance Characteristics
High memory usage for storing spectral state in DWDM systems.

## Research References
- ITU-T G.652 standard

## Implementation Notes
Implement split-step Fourier method for solving pulse propagation if high accuracy is demanded.

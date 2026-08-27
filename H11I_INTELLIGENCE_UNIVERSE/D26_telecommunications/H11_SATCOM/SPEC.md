> **Layer 2** · Telecommunications · `H11-SATCOM`

## Purpose

The H11-SATCOM agent models orbital communication networks, spanning LEO (Low Earth Orbit), MEO, and GEO constellations. It calculates dynamic ephemeris data, slant range, Doppler shifts, and atmospheric attenuation (rain fade).

## Technical Deep-Dive

It uses SGP4 orbital propagation algorithms to determine satellite positions and compute visibility windows for ground stations. It also manages Inter-Satellite Links (ISLs) and dynamic routing through the constellation mesh.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ground_lat | float | Latitude of ground station |
| ground_lon | float | Longitude of ground station |
| frequency_band | str | L, S, C, X, Ku, Ka, V |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| slant_range_km | float | Distance to satellite |
| elevation_angle | float | Elevation above horizon |
| link_margin_db | float | Available link margin |

### State Schema
Tracks full constellation TLEs (Two-Line Elements), current orbital states, and active ISL topology.

## Dependencies
- Upstream: None
- Downstream: H11-NETWORKING

## Failure Modes
- Loss of Line-of-Sight (LoS)
- Severe rain fade in Ka/V bands

## Performance Characteristics
High compute for continuous SGP4 propagation of thousands of LEO nodes.

## Research References
- SGP4 Orbital Model
- ITU-R P.618 (Rain attenuation)

## Implementation Notes
Implement spatial indexing for fast ground-to-sat visibility lookups.

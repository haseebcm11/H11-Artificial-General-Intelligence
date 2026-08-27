> **Layer 3** · Telecommunications · `H11-WIFI`

## Purpose

The H11-WIFI agent simulates indoor and dense urban Wireless Local Area Networks (802.11ax/be). It manages CSMA/CA contention mechanisms, spatial reuse (BSS coloring), and OFDMA resource unit (RU) allocations.

## Technical Deep-Dive

It explicitly models MAC layer collisions, exponential backoff, and Hidden Node problems in multi-AP environments. For Wi-Fi 7 (802.11be), it includes Multi-Link Operation (MLO) state tracking.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| ap_density | int | Access points per sq km |
| client_count | int | Total connected clients |
| protocol_version | str | e.g. "802.11ax" |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| mac_efficiency | float | Ratio of payload to raw airtime |
| collision_rate | float | Percentage of colliding frames |

### State Schema
Tracks BSSIDs, channel assignments, and ongoing TXOPs (Transmission Opportunities).

## Dependencies
- Upstream: H11-SPECTRUM
- Downstream: H11-NETWORKING

## Failure Modes
- Co-channel interference collapse
- Rogue AP disruptions

## Performance Characteristics
CSMA/CA slot-level simulation requires fine-grained temporal resolution.

## Research References
- IEEE 802.11ax/be standards
- Bianchi's Markov Model for DCF

## Implementation Notes
For large scale, approximate DCF using analytical Markov models rather than discrete event simulation per frame.

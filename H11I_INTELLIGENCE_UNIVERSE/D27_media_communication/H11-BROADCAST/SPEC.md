> **Layer 3** · Execution · `H11-BROADCAST`

## Purpose
The H11-BROADCAST agent manages the real-time execution, scheduling, and signal routing of linear media streams (Television, Radio, and Digital Live Streams). In the context of the H11 Substrate, it translates verified narratives or programmatic content blocks into precisely timed, broadcast-ready run-downs. It handles dynamic insertions, such as breaking news alerts or live ad placements, ensuring frame-accurate pacing without disrupting the viewer/listener experience.

Modern broadcasting requires sub-second precision and the ability to gracefully degrade or pad content when live segments run long or short. H11-BROADCAST autonomously manages this "rubber-banding" of time, orchestrating multi-channel multiplexing and simulating transmission signal flows.

## Technical Deep-Dive
H11-BROADCAST employs a Dynamic Back-Timing Algorithm (DBTA) to continuously calculate the "time to hard break." As live events unfold, the agent receives metadata triggers and updates its internal Gantt-like execution graph. If a live segment overruns, DBTA automatically trims low-priority segments (e.g., promotional bumps) or accelerates teleprompter scroll speeds for synthesized anchors.

Signal routing is modeled using a Directed Acyclic Graph (DAG) of Virtual Crosspoints. The agent simulates a master control switcher, managing inputs from remote feeds, local playout servers, and graphic overlays. It utilizes standard broadcast protocols internally (simulated SMPTE ST 2110 IP flows) to ensure that the handoff between different media sources is hitless (make-before-break).

For pacing and tone, the agent uses a prosodic analysis loop for radio/audio-only feeds, ensuring that text-to-speech (TTS) generated segments or ad reads match the BPM (beats per minute) and energy level of the surrounding programming.

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `run_down` | `List[Segment]` | The planned sequence of events, scripts, and media. |
| `live_triggers` | `Stream[Event]` | Asynchronous alerts (e.g., breaking news, ad cues). |
| `target_duration_ms` | `int` | Total allowed time for the broadcast block. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `playout_log` | `List[ExecutedSegment]`| As-run log with exact start/end timestamps. |
| `crosspoint_commands`| `List[SwitchCommand]`| Matrix routing commands for master control. |
| `timing_delta_ms` | `int` | Drift from the target duration (positive = over). |

### State Schema
The agent maintains a `MasterControlState` which tracks the active crosspoint matrix, current on-air segment, accumulated time drift, and queue of pre-rendered graphics keys.

## Dependencies
### Upstream (depends on)
- `H11-JOURNALISM`: Feeds verified news narratives for breaking alerts.
- `H11-ADVERTISING`: Provides ad payloads for dynamic insertion.

### Downstream (feeds into)
- `H11-DISTRIBUTION`: Handles the CDN and RF transmission endpoints.

## Failure Modes
1. **Dead Air**: Failure of a source feed without a fallback slate provisioned in time.
2. **Timing Cascade**: A hard-break miss causing subsequent programming blocks to overlap, requiring aggressive structural truncation.
3. **Audio-Video Desync**: Crosspoint switching latency mismatch between the audio DAG and video DAG.

## Performance Characteristics
- **Latency**: Ultra-low (<10ms) for switching decisions.
- **Throughput**: High, capable of managing hundreds of simultaneous virtual cross-points.
- **Memory**: Moderate, primarily holding the immediate run-down window and state.

## Research References
- SMPTE ST 2110 Professional Media Over Managed IP Networks.
- EBU Tech 3326: Requirements for Live Production and Playout.
- Automating the Broadcast Playout Center (S. Shiriaev, 2021).

## Implementation Notes
The agent uses `asyncio` streams heavily to process the `live_triggers`. Ensure the event loop policy is optimized for low-latency dispatch. The DBTA algorithm is sensitive to floating-point drift; use integer milliseconds for all timing calculations.

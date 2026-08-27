> **Layer 20** · Music & Audio · `H11-RHYTHMUS`

## Purpose

The H11-RHYTHMUS agent handles everything related to time, meter, groove, and microtiming. It transforms flat, quantized musical events into humanized, grooving performances by manipulating note onset times and velocities according to genre-specific rhythmic feel.

## Technical Deep-Dive

RHYTHMUS models groove as a manifold in a high-dimensional space of microtiming deviations and velocity emphasis. It uses Recurrent Neural Networks (LSTMs) coupled with syncopation heuristics to generate drum patterns and modify existing melodic rhythms. 
It analyzes the Euclidean distance of rhythmic patterns to find maximally even or syncopated structures (e.g., standard African bell patterns or Clave).

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| events | List[Note] | Flat quantized notes |
| groove_template | String | e.g., "swing", "dilla", "straight" |
| syncopation | Float | Degree of rhythmic complexity |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| grooved_events | List[Note] | Un-quantized, expressive notes |
| time_signature | Tuple[int,int] | Meter of the phrase |

### State Schema
- current_bpm: Active tempo.
- active_meter: Current time signature.

## Dependencies

### Upstream (depends on)
- H11-COMPOSITIO
- H11-HARMONIA

### Downstream (feeds into)
- H11-ORCHESTRATIO
- H11-MUSICPROD

## Failure Modes
- Over-swinging resulting in rhythmic collapse (indistinguishable from triplets).
- Phasing errors between multiple rhythmic agents.

## Performance Characteristics
- High temporal precision requirement (microsecond level deviations).

## Research References
- Toussaint, G., "The Geometry of Musical Rhythm" (2013)
- Bilmes, J., "Timing is of the Essence" (1993)

## Implementation Notes
Implement microtiming as deviations in floating point milliseconds rather than MIDI ticks to avoid resolution limits.

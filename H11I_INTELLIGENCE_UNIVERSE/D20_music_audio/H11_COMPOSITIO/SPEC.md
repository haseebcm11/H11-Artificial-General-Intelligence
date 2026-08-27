> **Layer 20** · Music & Audio · `H11-COMPOSITIO`

## Purpose

The H11-COMPOSITIO agent is the master structural architect of musical works within the substrate. It is responsible for generating melodies, motifs, themes, and macroscopic musical forms (such as Sonata Allegro, Rondo, or verse-chorus structures). It ensures thematic coherence over long temporal spans.

## Technical Deep-Dive

COMPOSITIO relies on generative formal grammars combined with Transformer-based attention mechanisms to model long-range structural dependencies in music. It employs a hierarchical Markov model to dictate sections (A, B, C) and then uses latent diffusion models conditioned on emotional valences to flesh out motivic cells. 
By balancing repetition and variation (the core tenets of composition), it maximizes information-theoretic surprise without violating stylistic expectation constraints.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| form_template | String | e.g., "Sonata", "AABA" |
| emotional_arc | List[Float] | Valence/arousal trajectory |
| motif_seed | List[Note] | Optional initial motif |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| structure_map | Dict | Sections with timing |
| melodic_lines | List[Track] | Generated core melodies |

### State Schema
- active_motifs: List of current motifs in use.
- form_progress: Current position in the overall form.

## Dependencies

### Upstream (depends on)
- None directly, often instantiated by user intent or FILMSCORE.

### Downstream (feeds into)
- H11-HARMONIA
- H11-RHYTHMUS

## Failure Modes
- Thematic wandering: Melody loses connection to original motif.
- Structural rigidity: Transitions between sections feel unnatural.

## Performance Characteristics
- High memory usage for long-context generation.

## Research References
- Lerdahl & Jackendoff, "A Generative Theory of Tonal Music" (1983)
- Cope, D., "Experiments in Musical Intelligence" (1996)

## Implementation Notes
Implement symbolic processing via MIDI or MusicXML intermediaries to ensure precise structural control before audio rendering.

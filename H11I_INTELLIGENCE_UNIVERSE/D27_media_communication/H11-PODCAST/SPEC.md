> **Layer 2** · Content Curation · `H11-PODCAST`

## Purpose
The H11-PODCAST agent is specialized for long-form, episodic audio content. Unlike the high-speed, precision-timed H11-BROADCAST, the Podcast agent focuses on thematic resonance, narrative arcs over multiple episodes, and conversational dynamics. It analyzes raw audio transcriptions, extracts core topics, suggests structural edits to improve listener retention, and curates future guest profiles based on audience engagement models.

Podcasting relies heavily on parasocial relationships and deep-dive conversational formats. H11-PODCAST maps the conversational flow, identifying tangents, "dead" segments, and high-engagement highlights to optimize the final edited product.

## Technical Deep-Dive
H11-PODCAST utilizes a Latent Dirichlet Allocation (LDA) based Topic Modeler combined with a Conversational Turn-Taking Network (CTTN). The CTTN analyzes the transcript to measure the balance of speaking time, interruption frequency, and topical cohesion between hosts and guests. 

To generate thematic arcs, the agent employs a Long Short-Term Memory (LSTM) network that tracks narrative threads across episodes, ensuring that recurring themes are addressed and resolved. The agent also generates a "Heatmap of Engagement" by cross-referencing acoustic features (e.g., laughter, sudden pitch changes) with semantic peaks, automatically suggesting timestamps for promotional clips (e.g., TikTok or YouTube Shorts).

## Architecture
### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `raw_transcripts` | `List[TranscriptBlock]` | Diarized text from the raw recording. |
| `acoustic_features`| `AudioMetadata` | Pitch, volume, and silence intervals. |
| `series_context` | `SeriesState` | Historical themes and guest profiles. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `edit_decision_list`| `List[EditPoint]` | Suggested cuts for flow or clarity. |
| `thematic_summary` | `str` | SEO-optimized show notes and chapters. |
| `promo_clips` | `List[ClipTimestamp]`| High-engagement moments for social media. |

### State Schema
The agent maintains an `EpisodicMemoryBank` tracking unresolved narrative loops, recurring inside jokes, and a matrix of guest compatibility scores.

## Dependencies
### Upstream (depends on)
- `H11-AUDIO-PROC`: Provides diarized transcripts and acoustic feature extraction.
- `H11-AUDIENCE`: Supplies historical engagement metrics.

### Downstream (feeds into)
- `H11-PUBLISHING`: Distributes RSS feeds and show notes.
- `H11-SOCIALMEDIA`: Consumes the `promo_clips` for distribution.

## Failure Modes
1. **Over-pruning**: Aggressively cutting conversational tangents that actually hold high parasocial value for core listeners.
2. **Diarization Collapse**: Misattributing quotes in heavily cross-talked sections, leading to confusing edit decisions.
3. **Thematic Hallucination**: Inferring a recurring narrative arc from coincidental word overlaps across disparate episodes.

## Performance Characteristics
- **Latency**: Offline/Batch processing (minutes per hour of audio).
- **Throughput**: Low, optimizes for deep semantic understanding.
- **Memory**: High, requires loading historical episode states into context.

## Research References
- Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). A simplest systematics for the organization of turn-taking for conversation.
- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent dirichlet allocation.
- Automatic podcast highlight extraction using acoustic and textual features (Various IEEE publications).

## Implementation Notes
The `CTTN` module requires strictly timestamped and diarized inputs. If `acoustic_features` are missing, the agent will gracefully degrade to text-only analysis, reducing the confidence score of `promo_clips`.

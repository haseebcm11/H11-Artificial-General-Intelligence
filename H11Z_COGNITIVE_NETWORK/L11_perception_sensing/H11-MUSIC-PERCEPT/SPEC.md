<<H11-MUSIC-PERCEPT — Music Perception>>
> **Layer 11** · Perception & Sensing · `H11-MUSIC-PERCEPT`

## Purpose
The H11-MUSIC-PERCEPT agent handles the highly specialized task of analyzing and understanding musical audio streams. While general audio perception handles speech and environmental noise, music perception requires distinct cognitive structures to process melody, harmony, rhythm, and timbre. This agent bridges raw audio waveforms to symbolic and structural musical representations, enabling the overarching cognitive system to understand context, mood, and temporal structures in music.

It operates by decomposing audio into frequency representations (e.g., Constant-Q Transforms) and processing them through specialized pipelines for onset detection, pitch tracking, and chord recognition, yielding a multidimensional semantic map of the musical content.

## Technical Deep-Dive
Music Information Retrieval (MIR) techniques form the backbone of this agent. It uses a combination of classic signal processing (like STFT and CQT) and deep learning models for feature extraction. The Constant-Q Transform (CQT) is heavily utilized as its logarithmic frequency scale closely matches human pitch perception and the Western musical scale. 

For rhythm and beat tracking, the agent employs Dynamic Bayesian Networks (DBNs) and Recurrent Neural Networks (RNNs) trained on onset detection functions. The onset detection relies on spectral flux and phase deviation, allowing the agent to pinpoint note attacks even in dense polyphonic mixtures. Beat tracking follows the Ellis (2007) dynamic programming approach, optimized for real-time streaming constraints.

Chord recognition and harmony analysis utilize Hidden Markov Models (HMMs) over chromagram sequences. Deep chromagrams, extracted via convolutional layers over the CQT, provide robustness against timbral variations. Instrument identification is handled by a separate branch of temporal-convolutional networks (TCNs) that analyze the spectral envelope and temporal evolution of individual sound events.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `audio_stream` | `np.ndarray` | Raw audio waveform data (typically 44.1kHz or 48kHz). |
| `sample_rate` | `int` | The sampling rate of the audio data. |
| `analysis_window` | `float` | Duration of the analysis window in seconds. |
| `features_requested` | `List[MusicFeature]` | Specific musical features to extract (e.g., beat, chord, genre). |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `tempo` | `float` | Estimated beats per minute (BPM). |
| `beats` | `List[BeatEvent]` | Temporal locations of detected beats and downbeats. |
| `chords` | `List[ChordSegment]` | Harmonic progression mapped over time. |
| `instruments` | `Dict[str, float]` | Probability distribution of detected instruments. |
| `structure` | `List[Section]` | Macro-structural analysis (e.g., verse, chorus). |

### State Schema
The agent maintains an acoustic memory buffer (`AcousticBuffer`) holding the last N seconds of audio for temporal context, a `FeatureCache` for storing intermediate representations (like CQT and Chromagrams) to avoid redundant computations across different analysis modules, and an `AnalysisTimeline` that progressively builds the structural map of the current musical piece.

## Dependencies
### Upstream
- `H11-AUDIO-SENSE`: Provides raw, pre-processed audio streams and basic environmental classification.
### Downstream
- `H11-EMOTION`: Uses musical context (tempo, harmony) for mood and affective state prediction.
- `H11-SCENE-UNDERSTAND`: Integrates background music semantics into the overall scene context.

## Failure Modes
1. **Polyphonic Masking**: Dense orchestral or heavily distorted music may mask individual pitches, degrading chord and instrument recognition.
2. **Tempo Drift in Expressive Timing**: Rubato or extreme tempo variations can confuse the beat tracking HMM, causing phase misalignment.
3. **Microtonal/Non-Western Scales**: Analysis heavily relying on 12-TET chromagrams may misinterpret microtonal music or non-Western tuning systems.
4. **Transient Smearing**: Aggressive audio compression upstream can smear transients, failing onset detection algorithms.
5. **Harmonic Aliasing**: Sub-harmonics or overtones from certain synthesizers might be misidentified as root notes.

## Performance Characteristics
- **Latency**: ~150ms for beat and pitch tracking; up to 2 seconds for structural boundaries.
- **Throughput**: Processes stereo 44.1kHz audio in real-time on standard CPU, with ~30% overhead on GPU for deep feature extraction.

## Research References
1. Ellis, D. P. (2007). *Beat tracking by dynamic programming*. Journal of New Music Research.
2. Böck, S., & Schedl, M. (2011). *Polyphonic piano note transcription with recurrent neural networks*. ICASSP.
3. McFee, Brian, et al. (2015). *librosa: Audio and music signal analysis in python*. Python in Science Conference.
4. Humphrey, E. J., & Bello, J. P. (2012). *Rethinking automatic chord recognition with convolutional neural networks*. ICMLA.

## Implementation Notes
Implementations must leverage optimized DSP libraries (e.g., FFTW, cuFFT) for CQT calculations. The chromagram generation should be cached as multiple modules (chord, structure, key) depend on it.

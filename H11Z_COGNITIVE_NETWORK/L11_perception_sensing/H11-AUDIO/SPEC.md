<<H11-AUDIO — Audio Perception>>
> **Layer 11** · Perception & Sensing · `H11-AUDIO`

## Purpose
The H11-AUDIO agent provides the cognitive substrate with generalized auditory perception. Unlike speech-specific processing, this agent focuses on the entire auditory landscape: background noises, sound events, musical elements, and acoustic environment characteristics. It translates raw waveform pressure changes into dense, rich acoustic representations.

## Technical Deep-Dive
H11-AUDIO operates primarily through two pathways: a deterministic signal processing frontend and a self-supervised neural backbone. 

The frontend computes Short-Time Fourier Transforms (STFT) and Mel-frequency cepstral coefficients (MFCCs). This provides a biologically inspired representation of auditory data emphasizing logarithmic frequency perception. 

The neural backbone employs models like HuBERT (Hidden-Unit BERT) and Wav2Vec2. These self-supervised encoders tokenize the continuous audio stream. HuBERT discovers acoustic units through k-means clustering of MFCCs and learns to predict these discrete units for masked regions of the audio, producing contextualized embeddings. For specific sound event detection (SED), an attached Convolutional Recurrent Neural Network (CRNN) processes the Mel-spectrograms to identify polyphonic sound events with high temporal resolution.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `waveform` | `NDArray[float32]` | Mono/Stereo audio array. |
| `sample_rate` | `int` | Hz (typically 16000 or 44100). |
| `extract_features` | `bool` | Whether to run self-supervised encoders. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `spectrogram` | `NDArray[float32]` | Mel-spectrogram matrix. |
| `embeddings` | `NDArray[float32]` | Dense feature embeddings from HuBERT. |
| `events` | `List[SoundEvent]` | Detected background audio events. |

### State Schema
Maintains `AudioBuffer` for streaming audio processing to handle overlaps and windowing accurately without edge artifacts.

## Dependencies
### Upstream
* Hardware interface layer (microphone array streams).
### Downstream
* `H11-SPEECH-IN`: Passes clean representations for ASR.
* `H12-CONTEXT`: Informs situational awareness (e.g., "sirens heard in background").

## Failure Modes
1. **Clipping Distortions**: Extreme amplitudes wrap/clip, destroying spectral features.
2. **Phase Cancellation**: Stereo to mono downmixing destroying out-of-phase signals.
3. **Domain Shift**: Self-supervised encoders hallucinating discrete units when exposed to ultrasonic or subsonic interference.

## Performance Characteristics
Frontend STFT completes in <5ms for 1-second chunks. HuBERT encoder requires ~15ms per second of audio on a modern GPU.

## Research References
1. Hsu, W. N., et al. (2021). "HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units."
2. Baevski, A., et al. (2020). "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations."
3. Mesaros, A., et al. (2021). "Sound event detection in the DCASE 2021 Challenge."

## Implementation Notes
Employs a streaming RingBuffer for STFT calculation to prevent memory fragmentation on long continuous streams.

> **Layer 3** · Perception & Actuation · `H11-SPEECH`

## Purpose

H11-SPEECH manages the acoustic interfaces of the cognitive substrate. It translates raw audio waveforms into structured text (ASR) and converts generated text back into highly expressive, human-like audio (TTS). For an AGI interacting with humans in real-time, low-latency and highly emotive speech processing is critical.

Unlike basic transcribers, this agent performs voice activity detection (VAD), speaker diarization (identifying "who spoke when"), and prosody extraction (detecting sarcasm, urgency, or hesitation). In synthesis, it utilizes voice cloning and emotional conditioning to generate speech that perfectly matches the required context.

## Technical Deep-Dive

For ASR, the agent utilizes End-to-End architectures like Conformer (Convolution-augmented Transformer) or Whisper, replacing traditional HMM/GMM pipelines. It processes Mel-filterbank features and uses Connectionist Temporal Classification (CTC) combined with attention-based decoding for robust alignment without frame-level labels.

For TTS, it employs non-autoregressive acoustic models (e.g., FastSpeech 2, VITS) paired with neural vocoders (e.g., HiFi-GAN) to synthesize raw waveforms directly from spectrograms. This bypasses the slow autoregressive sampling of older models (like WaveNet), achieving real-time factors (RTF) of < 0.05.

The agent handles continuous streaming audio via chunked processing and manages a dynamic context buffer to update transcriptions on the fly as subsequent acoustic context resolves earlier ambiguities.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| audio_stream | Stream[bytes] | Raw PCM or compressed audio data |
| task_type | SpeechTask | ASR, TTS, DIARIZATION, PROSODY |
| tts_text | Optional[str] | Text to synthesize (for TTS) |
| speaker_profile| Optional[str] | Voice ID for synthesis or diarization |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| transcript | str | Recognized text |
| synthesized_audio| bytes | Generated waveform |
| speaker_segments | List[Segment] | Timestamps mapped to speaker IDs |
| prosody_tags | Dict[str, float] | Detected emotion/tone |

### State Schema
- `active_streams`: Ring buffers for ongoing real-time ASR sessions.
- `voice_registry`: Cached speaker embeddings (d-vectors) for cloning.

## Dependencies

### Upstream (depends on)
- H11-GENERATIVA: Provides the text to be spoken.
- H11-EDGE: Captures microphone data.

### Downstream (feeds into)
- H11-NLP: Parses the generated transcripts.
- H11-MULTIMODALIS: Aligns audio features with video.

## Failure Modes
- `CocktailPartyDeafness`: Severe performance degradation when multiple speakers overlap without spatial audio separation.
- `VocoderArtifacts`: Synthesized speech exhibits robotic or metallic artifacts due to mismatch between the acoustic model and HiFi-GAN.
- `StreamingDesynchronization`: The chunked ASR decoder falls behind real-time, causing runaway latency accumulation.

## Performance Characteristics
- Latency (ASR): < 200ms for streaming word generation.
- Real-Time Factor (TTS): 0.05 (Generates 1 second of audio in 50ms).

## Research References
- Gulati, A., et al. (2020). *Conformer: Convolution-augmented Transformer for Speech Recognition*.
- Kim, J., et al. (2021). *Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech (VITS)*.

## Implementation Notes
Requires tight integration with C++ audio libraries (e.g., librosa, torchaudio) for low-latency feature extraction before neural processing.

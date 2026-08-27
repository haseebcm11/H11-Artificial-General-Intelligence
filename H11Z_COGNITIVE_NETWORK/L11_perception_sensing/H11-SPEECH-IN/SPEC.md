<<H11-SPEECH-IN — Speech Recognition (ASR)>>
> **Layer 11** · Perception & Sensing · `H11-SPEECH-IN`

## Purpose
The H11-SPEECH-IN agent is responsible for converting acoustic speech signals into structured text. It bridges acoustic perception and language understanding by employing state-of-the-art Automatic Speech Recognition (ASR). It is optimized for multi-lingual input, robust punctuation restoration, and seamless streaming capabilities for real-time interactions.

## Technical Deep-Dive
H11-SPEECH-IN implements a hybrid architectural strategy utilizing both an Attention-based Encoder-Decoder (AED) model (like Whisper) and a Connectionist Temporal Classification (CTC) pipeline. 

The CTC pipeline ensures ultra-low latency streaming by producing localized character/phoneme predictions synchronously with the audio frames. It uses a Wav2Vec2/Conformer backbone. 
The AED pipeline (Whisper) processes log-Mel spectrograms via a Vision-Transformer-like encoder and cross-attention text decoder. This provides immense robustness to noise, accents, and context, naturally handling translation and punctuation restoration implicitly via the language model fusion. 

Voice Activity Detection (VAD) preprocesses the streams to segment audio on silence boundaries, preventing decoder drift and hallucination during long non-speech segments.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `audio_chunk` | `NDArray[float32]` | 16kHz mono audio chunk. |
| `is_streaming` | `bool` | True for chunk-by-chunk CTC decoding. |
| `language` | `Optional[str]` | Language hint, or None for auto-detect. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `text` | `str` | Transcribed text. |
| `word_timestamps` | `List[WordSegment]` | Timing data for each word. |
| `is_final` | `bool` | True if the utterance is complete. |

### State Schema
Maintains `DecoderState` containing hidden states of the CTC beam search, and `VADState` tracking speech probability history to emit utterance boundaries.

## Dependencies
### Upstream
* `H11-AUDIO`: Often shares the spectrogram generation or raw waveform buffer.
### Downstream
* `H12-NLP`: Pushes transcribed text strings directly for parsing and intent recognition.

## Failure Modes
1. **Decoder Hallucination**: AED models looping phrases on pure silence or background noise. Mitigated by strict VAD gating.
2. **CTC Blank Collapse**: Beam search collapsing valid short phonemes into blank tokens on rapid, slurred speech.
3. **Punctuation Drift**: Multi-lingual decoding shifting syntax and misplacing punctuation due to language confusion.

## Performance Characteristics
Streaming CTC achieves ~150ms latency. AED batch processing operates at ~0.5x Real-Time Factor (RTF) on GPU.

## Research References
1. Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision." (Whisper)
2. Graves, A., et al. (2006). "Connectionist Temporal Classification: Labelling Unsegmented Sequence Data with Recurrent Neural Networks."
3. Gulati, A., et al. (2020). "Conformer: Convolution-augmented Transformer for Speech Recognition."

## Implementation Notes
To manage Whisper's 30-second context window limit, the agent implements a shifted-window dynamic chunking algorithm, anchoring context using overlapping 5-second segments.

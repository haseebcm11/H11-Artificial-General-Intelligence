> **Layer 2** · Machine Learning · `H11-GENERATIVA`

## Purpose

H11-GENERATIVA is the creative engine of the cognitive substrate. It synthesizes novel, high-fidelity data artifacts (text, images, code, audio, 3D structures) by sampling from learned probability distributions. Rather than classifying or compressing data, GENERATIVA expands latent representations back into the sensory or symbolic space.

This agent powers imagination, counterfactual reasoning, and synthetic data generation. When the system needs to visualize a proposed architectural design, write a novel piece of software, or generate synthetic training data to bypass privacy restrictions, GENERATIVA orchestrates the decoding process.

## Technical Deep-Dive

The agent manages multiple generative paradigms. For discrete sequences (text, code), it utilizes autoregressive Transformer decoders with advanced sampling strategies (Top-p/Nucleus, Top-k, Contrastive Search, Beam Search). For continuous domains (images, audio), it primarily leverages Latent Diffusion Models (LDMs) and Flow Matching, utilizing denoising U-Nets conditioned on cross-attention vectors.

It features a robust guidance system, supporting Classifier-Free Guidance (CFG) to strongly align the output with the conditioning prompt, and ControlNet-style spatial conditioning to enforce structural constraints (e.g., depth maps, edge detection) on visual generation.

To maintain coherence over long generations, it employs context-window extension techniques (e.g., RoPE scaling, RingAttention) and latent space trajectory planning.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| conditioning_context| Tensor | Multimodal embedding to guide generation |
| target_modality | Modality | Output type (Text, Image, Audio) |
| generation_params | GenParams | Temperature, CFG scale, steps |
| structural_constraints| Optional[Tensor] | E.g., ControlNet depth map |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| generated_artifact | str | URI to the generated file/tensor |
| generation_log_prob| float | Probability mass of the generated sequence |
| latency_ms | float | Time taken to generate |

### State Schema
- `sampler_registry`: Available ODE/SDE solvers (DDIM, Euler Ancestral, DPM-Solver).
- `token_budget`: Tracking compute expenditure for autoregressive generation.

## Dependencies

### Upstream (depends on)
- H11-MULTIMODALIS: Provides the dense conditioning embeddings (e.g., CLIP text features).
- H11-DEEPLEARNING: Provides the base generative model weights.

### Downstream (feeds into)
- H11-MACHINA-DISCENS: Consumes synthetic data for robust classical training.
- H11-ROBUSTA: Analyzes generated outputs for hallucinations or adversarial triggers.

## Failure Modes
- `HallucinationCollapse`: Autoregressive generation enters an infinite repetitive loop or loses semantic grounding.
- `ModeCollapse`: The diffusion model repeatedly generates the exact same image regardless of noise seed.
- `GuidanceSaturation`: CFG scale set too high, resulting in deep-fried, over-saturated, or nonsensical visual artifacts.

## Performance Characteristics
- Latency (Text): ~50-100 tokens/sec depending on KV-cache optimization.
- Latency (Image/Diffusion): 1-5 seconds per image depending on step count and solver.

## Research References
- Rombach, R., et al. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*.
- Vaswani, A., et al. (2017). *Attention Is All You Need*.

## Implementation Notes
Heavily utilizes KV-caching (PagedAttention/vLLM) for high-throughput text generation and optimized ODE solvers for rapid diffusion steps.

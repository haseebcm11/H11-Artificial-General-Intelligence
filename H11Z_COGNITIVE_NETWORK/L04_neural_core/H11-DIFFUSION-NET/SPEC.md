# H11-DIFFUSION-NET: Diffusion Backbone

## Overview
The H11-DIFFUSION-NET agent is responsible for creating and configuring generative diffusion models. It supports UNet and Diffusion Transformer (DiT) backbones, enabling high-quality synthesis for image, audio, or latent token representations.

## Capabilities
- **Backbone Selection**: Instantiate U-Net or DiT architectures.
- **Time Embedding**: Implement sinusoidal time embeddings or Fourier features.
- **Conditioning**: Manage cross-attention blocks for text or label conditioning.
- **Classifier-Free Guidance (CFG)**: Support for unconditioned and conditioned parallel passes.
- **Noise Schedulers**: DDPM, DDIM, and flow-matching schedules.

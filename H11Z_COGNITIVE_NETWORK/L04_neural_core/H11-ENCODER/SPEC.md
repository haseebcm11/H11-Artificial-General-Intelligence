# H11-ENCODER Agent Specification

## 1. Overview
The H11-ENCODER agent specializes in encoder-only architectures and their specific modality embeddings. It builds bidirectional representations suitable for tasks like Masked Language Modeling (BERT), Vision Processing (ViT), and Audio processing (Whisper).

## 2. Capabilities
- **Modality Patching**: Convert 2D images (ViT) or 1D audio spectrograms into sequence tokens.
- **Masking Strategies**: Generate corruption/masking masks for self-supervised training.
- **Bidirectional Attention**: Ensure causal masking is completely disabled, allowing full-context routing.
- **Classification Heads**: Provide standard `[CLS]` token pooling and projection heads.

## 3. Data Flow
Raw Modality -> Patching/Embedding -> Position Encoding -> H11-TRANSFORMER (Encoder Blocks) -> Pooling -> Output Task Head.

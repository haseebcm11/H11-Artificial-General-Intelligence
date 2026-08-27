<<H11-OCR — Optical Character Recognition>>
> **Layer 11** · Perception & Sensing · `H11-OCR`

## Purpose
The H11-OCR agent acts as the primary sensory interface for visual text and document structures. It translates pixel arrays containing typographic or handwritten elements into structured, machine-readable text and layout formats. This agent is essential for allowing the AGI to "read" screenshots, scanned documents, and in-the-wild scene text.

By integrating detection and recognition capabilities, H11-OCR bridges the gap between pure computer vision and natural language processing, ensuring textual data is accurately anchored to its spatial context.

## Technical Deep-Dive
H11-OCR operates in a multi-stage pipeline: Text Detection, Document Layout Analysis, and Text Recognition. For text detection, it employs a Differentiable Binarization (DBNet) algorithm that robustly identifies bounding polygons for text regions of arbitrary orientations. This avoids the limitations of traditional anchor-based object detectors when dealing with highly dense or curved text.

For Layout Analysis, it utilizes a multimodal transformer akin to LayoutLMv3, integrating spatial embeddings (bounding boxes) with image patches. This allows the agent to classify regions as headers, paragraphs, tables, or figures, establishing reading order and hierarchical document structure prior to OCR.

Recognition is handled by a Transformer-based OCR model (TrOCR), which bypasses traditional CNN-RNN-CTC architectures. The image patches of cropped text lines are encoded using a Vision Transformer (ViT) and decoded autoregressively into byte-pair encoded (BPE) tokens. This yields superior performance on complex cursive handwriting and heavily degraded historical documents.

## Architecture

### Input Contract
| Field | Type | Description |
|-------|------|-------------|
| `image_tensor` | `NDArray[float32]` | Normalized image array (C, H, W). |
| `dpi` | `int` | Resolution metadata for sizing heuristics. |
| `language_hints` | `List[str]` | ISO language codes to bias the decoder. |
| `layout_mode` | `LayoutMode` | Enum: RAW_TEXT, DOCUMENT, SCENE. |

### Output Contract
| Field | Type | Description |
|-------|------|-------------|
| `text_regions` | `List[TextRegion]` | Polygon bounds and transcribed text. |
| `layout_tree` | `DocumentNode` | Hierarchical DOM-like structure of the document. |
| `confidence` | `float` | Aggregate confidence score (0.0 to 1.0). |

### State Schema
Maintains a `ProcessingCache` tracking image hashes to avoid redundant OCR on static frames or duplicated documents. Holds active weights for the TrOCR and LayoutLM components.

## Dependencies
### Upstream
* `H11-VISION`: Relies on base vision encoders for initial feature extraction.
### Downstream
* `H12-SEMANTICS`: Feeds extracted text and reading order to semantic parsers.

## Failure Modes
1. **DPI Degradation**: Fails to detect micro-text when input tensor is aggressively downsampled.
2. **Reading Order Inversion**: Multi-column layouts incorrectly parsed across columns rather than down columns.
3. **Artifact Hallucination**: TrOCR autoregressive decoder looping or hallucinating repeated characters on blurry text.
4. **Watermark Interference**: High-contrast watermarks classified as scene text, breaking layout trees.

## Performance Characteristics
Operates at ~40ms for text detection per page, and ~100ms per 50 text lines for TrOCR decoding. Memory footprint is heavily bound to the ViT encoder size (approx 1.2GB VRAM).

## Research References
1. Liao, M., et al. (2020). "Real-time Scene Text Detection with Differentiable Binarization."
2. Li, M., et al. (2021). "TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models."
3. Huang, Y., et al. (2022). "LayoutLMv3: Pre-training for Document AI with Unified Text and Image Masking."

## Implementation Notes
To prevent decoder hallucination, a repetition penalty is enforced in the beam search decoding phase of the TrOCR module.

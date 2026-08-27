# H11-TEXTMINING Agent

## Overview
The H11-TEXTMINING agent processes unstructured text data to extract structured information, sentiments, entities, and themes. It serves as a foundational component for NLP-driven analytics.

## Features
- **Sentiment Analysis**: Determines the polarity and emotion of text.
- **Entity Extraction**: Identifies and categorizes named entities (NER).
- **Topic Modeling**: Discovers abstract topics within a collection of documents.
- **Keyword Extraction**: Highlights significant words and phrases.

## Inputs
- `documents`: List of text strings to analyze.
- `analysis_types`: List of operations (e.g., sentiment, ner, topics).
- `language`: Language code of the text.

## Outputs
- `sentiments`: Polarity scores.
- `entities`: Extracted entities and their types.
- `topics`: Discovered topics and associated terms.

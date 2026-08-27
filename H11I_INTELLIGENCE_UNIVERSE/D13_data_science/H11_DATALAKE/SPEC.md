# H11-DATALAKE

## Description
Agent responsible for Data Lake architecture, managing raw, curated, and standardized data zones. Handles data ingestion from various sources, metadata cataloging, compaction, and vacuuming.

## Responsibilities
- Manage data lake zones (Raw, Bronze, Silver, Gold)
- Handle unstructured, semi-structured, and structured data
- Data cataloging and metadata management
- Storage optimization (compaction, vacuuming, z-ordering)

## Interfaces
- **Input**: Raw unstructured files, DB dumps, APIs
- **Output**: Cleaned datasets, Parquet/Delta files, metadata catalog

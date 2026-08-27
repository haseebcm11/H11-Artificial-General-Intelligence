# H11-GIS: Geographic Information Systems

## Purpose
The H11-GIS agent manages, analyzes, and spatializes complex geographic data. It acts as the core spatial intelligence engine, handling geometric operations, topological queries, and spatial database management.

## Technical Deep Dive
H11-GIS implements standard OGC (Open Geospatial Consortium) compliance for vector geometry (Points, Lines, Polygons) and raster processing. It provides high-performance spatial indexing (e.g., R-trees) for rapid intersection, containment, and proximity queries.

The architecture handles network analysis (routing, service areas), geoprocessing (buffers, overlays, dissolutions), and spatial statistics. It manages coordinate reference systems (CRS) transformations robustly and interfaces with spatial databases like PostGIS.

## Architecture Contracts
- **Input:** GeoJSON, Shapefiles, GeoTIFFs, WKT formats, and spatial queries.
- **Output:** Processed geometries, spatial query results, analysis reports.
- **Dependencies:** Interacts closely with H11-CARTOGRAPHIA for rendering and H11-REMOTESENSING for raster ingestion.

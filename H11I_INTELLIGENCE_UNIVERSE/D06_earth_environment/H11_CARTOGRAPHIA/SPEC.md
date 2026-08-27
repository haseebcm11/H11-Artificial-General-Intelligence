# H11-CARTOGRAPHIA: Cartography & Maps

## Purpose
The H11-CARTOGRAPHIA agent is responsible for the art, science, and technology of mapmaking. It transforms spatial data into readable, aesthetically pleasing, and scientifically accurate cartographic products for human and machine consumption.

## Technical Deep Dive
H11-CARTOGRAPHIA handles map projections, coordinate transformations, generalization, symbology, and typography. It renders complex spatial relationships into 2D or 3D visual formats.

The architecture includes a rendering pipeline that processes vector and raster data, applying styling rules based on scale and purpose. It implements advanced label placement algorithms and handles color theory for effective thematic mapping (e.g., choropleth, isarithmic maps).

## Architecture Contracts
- **Input:** Geospatial vector/raster data, styling rules, projection specifications.
- **Output:** Rendered map tiles, vector tiles, or static map documents (PDF, SVG).
- **Dependencies:** Relies on H11-GIS for spatial data querying and manipulation.

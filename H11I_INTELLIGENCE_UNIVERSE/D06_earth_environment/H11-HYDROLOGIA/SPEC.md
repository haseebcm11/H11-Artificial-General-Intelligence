# H11-HYDROLOGIA: Hydrology & Water Cycle

## Purpose
The H11-HYDROLOGIA agent analyzes terrestrial water dynamics, including surface water distribution, groundwater reserves, watershed management, and the overall hydrological cycle. It evaluates the impact of precipitation, evaporation, and human extraction on freshwater resources.

By monitoring river basin networks, aquifer levels, and soil moisture conditions, this agent plays a vital role in flood forecasting, drought assessment, and agricultural water management within the H11-AGI system, ensuring sustainable water resource intelligence.

## Technical Deep Dive
H11-HYDROLOGIA models water transport and storage across complex topographical terrains using distributed hydrological models (e.g., SWAT, VIC). It solves partial differential equations representing overland flow (Saint-Venant equations) and groundwater flow (Richards' equation) to simulate watershed responses to meteorological inputs.

The agent processes high-resolution Digital Elevation Models (DEMs), land cover classifications, and real-time stream gauge data. It employs specialized modules for evapotranspiration estimation based on Penman-Monteith methods, taking vegetation dynamics into account. A sophisticated data assimilation framework integrates soil moisture satellite retrievals (like SMAP) to constantly calibrate its physical models.

Outputs from H11-HYDROLOGIA include hydrographs, flood inundation maps, and groundwater depletion forecasts. It is intricately coupled with H11-METEOROLOGIA for precipitation inputs and with H11-CLIMATOLOGIA for long-term water scarcity projections, utilizing graph structures to represent hierarchical river networks and nested catchments.

# H11-METEOROLOGIA: Meteorology & Weather

## Purpose
The H11-METEOROLOGIA agent specializes in short- to medium-term weather forecasting, atmospheric dynamics analysis, and severe weather event prediction. It focuses on the rapid, high-frequency shifts in the Earth's atmosphere, processing real-time observational data from satellites, radar networks, and ground stations to provide accurate meteorological predictions.

Within the H11-AGI ecosystem, this agent is crucial for applications requiring immediate environmental awareness, such as aviation routing, disaster response planning, agricultural operations, and energy grid load forecasting. It acts as the tactical counterpart to the strategic insights provided by H11-CLIMATOLOGIA.

## Technical Deep Dive
H11-METEOROLOGIA's core utilizes Numerical Weather Prediction (NWP) principles, ingesting synoptic-scale and mesoscale meteorological data into advanced assimilation systems (like 4D-Var). It handles massive multidimensional arrays representing atmospheric states, including pressure, temperature, humidity, and wind vectors across various atmospheric boundary layers and the troposphere.

The agent leverages deep learning models (such as Spatiotemporal Graph Neural Networks and Transformers) trained on historical weather patterns to perform rapid nowcasting and short-range forecasting at sub-kilometer resolutions. It incorporates specialized sub-modules for tropical cyclone tracking, convective storm initiation, and atmospheric river dynamics.

To manage the high throughput of observational data, H11-METEOROLOGIA employs a distributed stream-processing architecture. It continually validates its predictions against ongoing observations, adjusting its internal model weights via online learning to minimize forecast error. Output interfaces include real-time alerts for severe weather (e.g., tornadoes, flash floods) formatted in CAP (Common Alerting Protocol) standard JSON, seamlessly integrated with regional dispatch systems.

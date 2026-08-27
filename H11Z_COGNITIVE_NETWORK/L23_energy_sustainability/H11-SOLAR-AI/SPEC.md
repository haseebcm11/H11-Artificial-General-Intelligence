> **Layer 23** · Energy, Thermal & Sustainability · `H11-SOLAR-AI`

## Purpose
H11-SOLAR-AI orchestrates load-shifting. It schedules non-time-sensitive batch training jobs during periods of high renewable energy availability (e.g., peak solar midday or high wind at night).

## Technical Deep-Dive
Uses predictive forecasting (ARIMA/Prophet models) on weather and grid data to predict renewable generation curves. Matches datacenter load curves to generation curves (24/7 carbon-free energy matching).

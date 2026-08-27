# H11-AB Agent

## Overview
The H11-AB agent specializes in experimental design and A/B testing analysis. It helps in validating hypotheses by comparing variants and calculating statistical significance.

## Features
- **Experiment Design**: Recommends sample sizes and test durations.
- **Significance Testing**: Performs t-tests, chi-squared tests, or Bayesian analysis.
- **Conversion Rate Optimization (CRO)**: Identifies winning variations.
- **Segmentation Analysis**: Determines if specific user groups behave differently.

## Inputs
- `experiment_data`: Conversion and traffic data for variants.
- `metric_type`: Type of metric (binomial, continuous).
- `confidence_level`: Required statistical confidence (e.g., 0.95).

## Outputs
- `winner`: The winning variant, if any.
- `p_value`: Probability value.
- `lift`: Percentage improvement over the control.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-01

### Added

- Core diagnostic coordinate computation (`compute_x_y`)
  - Computes x = p2/p1 and y = (1-x)^(-1/2)
  - Requires semantic metadata (p1_name, p2_name, failure_definition)
  - Validates inputs and issues warnings near capacity threshold
  - Clips x to prevent numerical divergence as x approaches 1

- Uncertainty propagation (`bootstrap_ci`, `delta_method_ci`)
  - Bootstrap confidence intervals for x and y
  - Delta method confidence intervals with optional covariance
  - Reproducible with random_state parameter

- Validation utilities (`collapse_test`, `negative_control_plot`, `sensitivity_check`)
  - Collapse test for comparing multiple datasets
  - Negative control generation via shuffling
  - Sensitivity analysis for perturbations in p1 and p2

- Documentation
  - README with scope box and usage examples
  - Full scope documentation (docs/scope.md)
  - Misuse cases (docs/how_not_to_use.md)
  - Reproducibility checklist (docs/checklist.md)

- Examples
  - Synthetic demo notebook (examples/synthetic_demo.ipynb)

- Tests
  - Unit tests for core functionality
  - Unit tests for validation utilities
  - Tests for input validation and warnings
  - Tests for numerical stability near x = 1

### Notes

- This is a diagnostic tool only
- Does not infer p1 or p2 from data
- Does not predict system failure
- Does not model dynamics
- Does not claim universality

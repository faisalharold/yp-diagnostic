# Release Notes: v1.0.0

**Release Date:** 2025-01-01
**Type:** Initial diagnostic release

---

## Summary

`yp-diagnostic` v1.0.0 provides a diagnostic coordinate for finite systems near capacity thresholds. This release implements the core computation, uncertainty propagation, and validation utilities.

---

## Scope

This package computes:
- **x = p₂ / p₁** (ratio of comparison to reference value)
- **y = (1 - x)^(-1/2)** (diagnostic coordinate)

The diagnostic coordinate **indicates** when x approaches 1. It **flags** a regime where small changes in x produce large changes in y.

---

## Non-Claims

This package explicitly does **NOT**:

| Claim | Status |
|-------|--------|
| Predict system failure | ✗ Not supported |
| Model system dynamics | ✗ Not supported |
| Infer p₁ or p₂ from data | ✗ Not supported |
| Claim universality | ✗ No such claims |
| Imply causation or mechanism | ✗ No such claims |
| Validate real-world applicability | ✗ Requires independent validation |

**Any application to real systems requires independent, domain-specific validation.**

---

## What's Included

### Core Functions
- `compute_x_y`: Computes diagnostic coordinate with semantic guardrails
- `bootstrap_ci`: Uncertainty propagation via bootstrap
- `delta_method_ci`: Uncertainty propagation via delta method

### Validation Utilities
- `collapse_test`: Compare multiple datasets
- `negative_control_plot`: Generate shuffled controls
- `sensitivity_check`: Analyze perturbation sensitivity

### Documentation
- `docs/scope.md`: Full scope and assumptions
- `docs/how_not_to_use.md`: Misuse cases
- `docs/checklist.md`: Reproducibility checklist
- `docs/validation_protocol.md`: Validation methodology
- `docs/reproducibility_statement.md`: Reproducibility statement

### Tests
- 64 unit tests covering all functionality
- Tests for input validation, warnings, and numerical stability

---

## Requirements

- Python >= 3.9
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.4.0

---

## Citation

```bibtex
@software{yp_diagnostic,
  author = {Harold, Faisal},
  title = {A Diagnostic Coordinate for Finite Systems Near Capacity Thresholds},
  version = {1.0.0},
  year = {2025},
  url = {https://github.com/faisalharold/yp-diagnostic}
}
```

See `CITATION.cff` for machine-readable citation information.

---

## License

MIT License. See `LICENSE` file.

---

## Breaking Changes Policy

Per semantic versioning, breaking changes to the public API will require a major version increment (v2.0.0).

---

*This is a diagnostic tool only. It does not predict, model, or validate system behavior.*

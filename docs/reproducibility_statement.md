# Reproducibility Statement

This document mirrors the reproducibility language from the associated manuscript. It is provided for reference only and does not introduce new claims.

---

## Code and Data Availability

The `yp-diagnostic` package is available at:
- Repository: https://github.com/faisalharold/yp-diagnostic
- Version: 1.0.0
- License: MIT

All code required to reproduce the diagnostic coordinate computation is included in this repository.

---

## Software Dependencies

The package requires:
- Python >= 3.9
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.4.0

These dependencies are standard scientific Python packages with stable APIs.

---

## Reproducibility of Results

### Synthetic Demonstration

The synthetic demonstration (`examples/synthetic_demo.ipynb`) uses:
- Fixed random seed (`np.random.seed(42)`)
- Explicit parameter values (p₁ = 1000, p₂ varies from 100 to 990)
- Reproducible bootstrap sampling (`random_state=42`)

Running the notebook should produce identical numerical results across executions.

### Unit Tests

All 64 unit tests are deterministic and should pass on any system meeting the dependency requirements:

```bash
pip install -e .
pytest tests/ -v
```

---

## What This Package Reproduces

This package reproduces the computation of:
- x = p₂ / p₁
- y = (1 - x)^(-1/2)

for user-supplied values of p₁ and p₂.

---

## What This Package Does NOT Reproduce

This package does not reproduce:
- Any empirical findings from real-world systems
- Any predictions about system behavior
- Any claims about universality or mechanism

The synthetic demonstration is illustrative only and does not constitute validation of real-world applicability.

---

## Verification Checklist

Before claiming reproducibility, verify:

- [ ] Package installs without errors
- [ ] All unit tests pass
- [ ] Synthetic notebook runs without errors
- [ ] Numerical outputs match expected values (see notebook)
- [ ] Warnings trigger appropriately (x >= 0.9, x >= 1.0)

---

## Contact

For reproducibility issues, open an issue at:
https://github.com/faisalharold/yp-diagnostic/issues

---

*This document is part of the yp-diagnostic package (v1.0.0) and does not introduce claims beyond those in the associated manuscript.*

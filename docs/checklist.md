# Reproducibility Checklist

Use this checklist to ensure reproducible and appropriate use of the `yp-diagnostic` package.

---

## Before Computing y(p)

### Data Preparation

- [ ] p1 values are explicitly defined (not inferred from data)
- [ ] p2 values are explicitly defined (not inferred from data)
- [ ] p1 values are strictly positive
- [ ] p2 values are non-negative
- [ ] Units of p1 and p2 are consistent and documented

### Metadata

- [ ] `p1_name` clearly describes what p1 represents
- [ ] `p2_name` clearly describes what p2 represents
- [ ] `failure_definition` explicitly states what failure means
- [ ] Metadata is specific enough for independent reproduction

### Scope Understanding

- [ ] I understand that y(p) is a diagnostic coordinate, not a prediction
- [ ] I understand that high y does not predict or cause failure
- [ ] I understand that no inference or modeling is performed
- [ ] I have read `docs/scope.md`
- [ ] I have read `docs/how_not_to_use.md`

---

## During Computation

### Warnings

- [ ] I have not suppressed warnings
- [ ] I have documented any warnings that occur
- [ ] I understand what each warning means

### Numerical Stability

- [ ] I am aware that y is clipped when x >= 0.999999
- [ ] I have checked for NaN or Inf values in outputs
- [ ] I have verified that results are numerically reasonable

---

## Uncertainty Propagation

### Bootstrap CI

- [ ] Random seed is set for reproducibility (`random_state` parameter)
- [ ] Number of bootstrap samples is documented (`n_boot`)
- [ ] I understand the assumptions (see docstring)
- [ ] For scalar inputs: p1_std and p2_std are provided
- [ ] For array inputs: observations are paired appropriately

### Delta Method CI

- [ ] I understand the assumptions (see docstring)
- [ ] Standard errors are small relative to point estimates
- [ ] Covariance between p1 and p2 is specified if non-zero

---

## Validation Utilities

### Collapse Test

- [ ] I understand that collapse is definitional, not a discovery
- [ ] I have not claimed "universal scaling" based on overlap
- [ ] Labels are provided for all datasets

### Negative Controls

- [ ] Random seed is set for reproducibility
- [ ] I understand this is exploratory, not a hypothesis test
- [ ] I have not claimed statistical significance from this utility

### Sensitivity Check

- [ ] Perturbation fractions are documented
- [ ] I have not determined "acceptable" sensitivity (only reported)
- [ ] Results are used for exploration, not validation

---

## Reporting Results

### Language

- [ ] I use "diagnostic coordinate" or "transformed ratio"
- [ ] I do NOT use "universal," "fundamental," or "law"
- [ ] I do NOT claim prediction, causation, or mechanism
- [ ] I do NOT claim detection of phase transitions or criticality

### Documentation

- [ ] Exact version of `yp-diagnostic` is recorded (1.0.0)
- [ ] All input values (p1, p2) are documented
- [ ] All metadata (p1_name, p2_name, failure_definition) is documented
- [ ] Random seeds are documented for reproducibility
- [ ] Any warnings are documented

### Interpretation

- [ ] I state what y(p) shows (proximity to x = 1)
- [ ] I state what y(p) does NOT show (prediction, mechanism, causation)
- [ ] I acknowledge limitations of the diagnostic
- [ ] I do not overinterpret results

---

## Code Quality

### Testing

- [ ] Unit tests pass (`pytest tests/`)
- [ ] Edge cases are tested (x near 1, x = 0, arrays)
- [ ] Invalid inputs raise appropriate errors

### Dependencies

- [ ] Python >= 3.9
- [ ] NumPy >= 1.20.0
- [ ] SciPy >= 1.7.0
- [ ] Matplotlib >= 3.4.0 (for visualization only)

---

## Final Check

Before publishing or sharing results:

- [ ] README scope matches actual usage
- [ ] No claims beyond diagnostic interpretation
- [ ] Reproducibility information is complete
- [ ] Code and data are archived with version information

---

## Quick Reference

| Do | Don't |
|---|---|
| Provide explicit p1 and p2 | Infer p1 or p2 from data |
| Use descriptive metadata | Use vague or placeholder metadata |
| Report y as a diagnostic | Claim y predicts failure |
| Document all parameters | Omit reproducibility details |
| Read and report warnings | Suppress warnings silently |
| Acknowledge limitations | Claim universality or mechanism |

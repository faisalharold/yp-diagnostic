# Validation Protocol

This document mirrors the validation methodology from the associated manuscript Methods section. It is provided for reference only and does not introduce new claims.

---

## Overview

The validation protocol examines whether the diagnostic coordinate y(p) organizes observations in a manner consistent with proximity to a capacity threshold. This protocol does **not** validate prediction, mechanism, or universality.

---

## Protocol Steps

### Step 1: Define p₁ and p₂ Explicitly

Before computing y(p), explicitly define:
- **p₁**: The reference value (e.g., capacity, threshold, maximum)
- **p₂**: The comparison value (e.g., load, usage, current level)
- **Failure definition**: What constitutes failure in this context

These values must be:
- Measured or specified independently (not inferred from y)
- Positive (p₁ > 0) and non-negative (p₂ >= 0)
- Meaningful in the application domain

### Step 2: Compute x and y

Using the `yp-diagnostic` package:

```python
from yp_diagnostic import compute_x_y

x, y = compute_x_y(
    p1=p1_value,
    p2=p2_value,
    p1_name="explicit_description_of_p1",
    p2_name="explicit_description_of_p2",
    failure_definition="explicit_definition_of_failure"
)
```

### Step 3: Negative Controls

Examine whether the diagnostic coordinate captures information beyond the individual components:

1. **Outcome vs p₁ alone**: Plot outcome against p₁ only
2. **Outcome vs p₂ alone**: Plot outcome against p₂ only
3. **Outcome vs x**: Plot outcome against x = p₂/p₁
4. **Outcome vs y**: Plot outcome against y = (1-x)^(-1/2)

If y provides no additional organization beyond x, p₁, or p₂, the diagnostic may not be informative for the specific application.

### Step 4: Sensitivity Analysis

Examine sensitivity of y to measurement uncertainty:

```python
from yp_diagnostic import sensitivity_check

result = sensitivity_check(p1=p1_value, p2=p2_value)
```

Report how y changes with perturbations in p₁ and p₂.

### Step 5: Shuffled Controls

Compare observed y values against shuffled baselines:

```python
from yp_diagnostic import negative_control_plot

result = negative_control_plot(p1=p1_array, p2_real=p2_array, n_shuffles=100)
```

This is exploratory, not a statistical test.

---

## What This Protocol Validates

This protocol can assess whether:
- y organizes observations by proximity to x = 1
- The relationship between y and outcomes (if any) differs from random baseline
- y is sensitive to measurement uncertainty

---

## What This Protocol Does NOT Validate

This protocol does **not** validate:
- That y predicts system failure
- That y reflects any causal mechanism
- That y is universal across systems
- That the diagnostic is appropriate for any specific application

---

## Reporting Requirements

When reporting results using this protocol, include:

1. Explicit definitions of p₁, p₂, and failure
2. Sample sizes and data sources
3. All plots from Step 3 (negative controls)
4. Sensitivity analysis results
5. Any warnings issued by the package

Do **not** claim:
- Prediction capability
- Mechanistic understanding
- Universality
- Validation of real-world applicability (unless independently demonstrated)

---

## Limitations

This validation protocol:
- Does not perform hypothesis testing
- Does not compute p-values
- Does not determine statistical significance
- Does not validate theoretical claims

It provides diagnostic visualization only.

---

*This document is part of the yp-diagnostic package (v1.0.0) and mirrors the Methods section of the associated manuscript. It does not introduce claims beyond those in the manuscript.*

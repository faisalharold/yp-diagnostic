# Scope and Assumptions

This document defines the scope, assumptions, and limitations of the `yp-diagnostic` package.

---

## What This Package Does

This package computes a diagnostic coordinate for finite systems near capacity thresholds:

- **x = p2 / p1**: The ratio of a comparison value (p2) to a reference value (p1)
- **y = (1 - x)^(-1/2)**: A coordinate that increases as x approaches 1

The package also:

- Propagates uncertainty from p1 and p2 into y
- Enforces semantic guardrails via required metadata
- Provides validation utilities for exploratory analysis

---

## What This Package Does NOT Do

This package explicitly does NOT:

1. **Infer p1 or p2**: Users must provide explicit values. No fitting, estimation, or inference is performed.

2. **Model dynamics**: No time evolution, differential equations, or dynamical systems modeling.

3. **Predict transitions**: The diagnostic coordinate y does not predict when or if a system will fail.

4. **Detect chaos or criticality**: No claims about phase transitions, critical phenomena, or emergent behavior.

5. **Claim universality**: The y(p) coordinate is specific to the (1-x)^(-1/2) transformation. No claims about general applicability.

6. **Use machine learning**: No neural networks, regression models, or data-driven inference.

7. **Use external datasets**: No pre-loaded data, benchmarks, or reference systems.

---

## Mathematical Definition

Given:
- p1: A positive reference value (e.g., capacity)
- p2: A non-negative comparison value (e.g., load)

The diagnostic coordinates are:

```
x = p2 / p1
y = (1 - x)^(-1/2)
```

### Properties

- y = 1 when x = 0
- y increases monotonically as x increases
- y diverges as x → 1
- y is undefined for x ≥ 1 (numerically clipped in implementation)

---

## Required Inputs

All computations require:

1. **p1**: Positive scalar or array (reference value)
2. **p2**: Non-negative scalar or array (comparison value)
3. **p1_name**: String describing what p1 represents
4. **p2_name**: String describing what p2 represents
5. **failure_definition**: String describing what constitutes failure

The metadata requirements (p1_name, p2_name, failure_definition) are enforced to ensure:
- Explicit semantic context for the diagnostic
- Interpretability of results
- Prevention of casual misuse

---

## Assumptions

### Mathematical Assumptions

1. **p1 > 0**: The reference value must be strictly positive to avoid division by zero.
2. **p2 ≥ 0**: The comparison value must be non-negative.
3. **x < 1 for finite y**: When x ≥ 1, y is clipped to prevent numerical divergence.

### Interpretation Assumptions

1. **Ratio is meaningful**: The ratio p2/p1 has a well-defined interpretation in the user's domain.
2. **Threshold at x = 1**: The value x = 1 represents a meaningful threshold (e.g., load equals capacity).
3. **No hidden variables**: The relationship between p1 and p2 is direct, not mediated by unobserved factors.

### Uncertainty Propagation Assumptions

For `bootstrap_ci`:
- Scalar inputs: p1 and p2 are assumed normally distributed with provided standard deviations.
- Array inputs: Paired observations are assumed to be independent.

For `delta_method_ci`:
- First-order Taylor approximation is adequate.
- p1 and p2 are approximately normally distributed.
- Standard errors are small relative to point estimates.

---

## Limitations

### Numerical Limitations

1. **Clipping near x = 1**: When x ≥ 0.999999, the value is clipped to prevent infinite y.
2. **Floating point precision**: Near-capacity values may have reduced numerical precision.

### Interpretive Limitations

1. **Descriptive only**: y describes where x is relative to 1; it does not explain why.
2. **No prediction**: High y does not predict that failure will occur.
3. **No mechanism**: y does not reveal underlying mechanisms or causal relationships.
4. **Context-dependent**: The meaning of y depends entirely on what p1 and p2 represent.

### Validation Limitations

1. **No ground truth**: Validation utilities report diagnostics; they do not verify correctness.
2. **No significance testing**: No p-values or hypothesis tests are provided.
3. **No model comparison**: No tools for comparing alternative specifications.

---

## Appropriate Use Cases

This package may be appropriate when:

1. You have explicit measurements of p1 and p2.
2. The ratio p2/p1 has a clear interpretation.
3. You want to flag when this ratio approaches 1.
4. You understand that y is a diagnostic coordinate, not a prediction.

---

## Inappropriate Use Cases

See `how_not_to_use.md` for detailed misuse cases.

---

## Version

This document applies to version 1.0.0 of the `yp-diagnostic` package.

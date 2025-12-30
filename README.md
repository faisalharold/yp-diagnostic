# yp-diagnostic

A diagnostic coordinate for finite systems near capacity thresholds.

> ⚠️ **CRITICAL**: This is a **diagnostic tool**, not a predictive model or physical law.
>
> The coordinate y(p) = (1 - p₂/p₁)^(-1/2) is a mathematical reparameterization
> chosen for its divergent behavior near x = 1. It does not predict system failure,
> explain system dynamics, apply universally, or detect critical phenomena.
>
> Any use beyond diagnostic flagging requires independent, domain-specific validation.

---

## System Requirements

This diagnostic is designed **only** for systems where:

1. **The system is finite**: There exists a meaningful, fixed capacity or threshold (p₁)
2. **Failure is absorbing**: Once the threshold is reached or exceeded, the system does not spontaneously recover
3. **p₁ and p₂ are externally defined**: Values are measured or specified independently, never inferred from y or from failure observations

**Do not use this diagnostic for:**
- Reversible systems (where load can decrease and recovery is automatic)
- Infinite or unbounded systems (where no capacity threshold exists)
- Elastic systems that auto-scale (where p₁ is not fixed)
- Systems where p₁ must be estimated from observed failures

---

## Scope

### What this package does

- Computes a diagnostic coordinate: `x = p2 / p1` and `y = (1 - x)^(-1/2)`
- Propagates uncertainty through bootstrap and delta method confidence intervals
- Enforces semantic guardrails via required metadata (p1_name, p2_name, failure_definition)
- Warns when x approaches 1 (near capacity)
- Provides validation utilities for sensitivity checking

### What this package does NOT do

- **Does not infer** p1 or p2 from data
- **Does not model** system dynamics
- **Does not predict** transitions or future states
- **Does not detect** chaos or critical phenomena
- **Does not claim** universality, causality, or mechanism
- **Does not use** machine learning or external datasets

---

## Installation

```bash
pip install .
```

Or for development:

```bash
pip install -e .
```

Requires Python >= 3.9, NumPy, SciPy, Matplotlib.

---

## Minimal Example

```python
from yp_diagnostic import compute_x_y

# Explicit capacity and load values with required semantic metadata
p1 = 100.0  # capacity
p2 = 85.0   # current load

x, y = compute_x_y(
    p1=p1,
    p2=p2,
    p1_name="server_capacity_requests_per_sec",
    p2_name="current_load_requests_per_sec",
    failure_definition="response_time_exceeds_500ms"
)

print(f"x = {x:.3f}, y = {y:.3f}")
# x = 0.850, y = 2.582
```

---

## Interpretation

The coordinate y(p) = (1 - p2/p1)^(-1/2) **indicates** when a ratio-based metric (x = p2/p1) is approaching 1.

- **y increases** monotonically as x approaches 1
- **y diverges** as x → 1
- This **flags** a regime where small changes in x produce large changes in y

**What this indicates:** The system is near a threshold where rate-based metrics may become unreliable due to survival conditioning or capacity limits.

**What this does NOT indicate:** Causation, prediction of failure, mechanism of transition, or universality of behavior.

> **This is a diagnostic coordinate, not a mechanistic model.** It does not predict system behavior. Any application to real systems requires independent, domain-specific validation.

### Interpretation Table

| x = p₂/p₁ | y = (1-x)^(-1/2) | Interpretation |
|-----------|------------------|----------------|
| 0.00 | 1.00 | Ratio is zero; no proximity to threshold |
| 0.50 | 1.41 | Half capacity; low x regime |
| 0.80 | 2.24 | 80% capacity; moderate x regime |
| 0.90 | 3.16 | 90% capacity; high x regime (warnings issued) |
| 0.95 | 4.47 | 95% capacity; high x regime |
| 0.99 | 10.0 | 99% capacity; near-threshold |
| ≥1.00 | clipped (~1000) | At or beyond threshold; clipped for numerical stability |

**What these values mean:** y quantifies how close x is to 1. Higher y = closer to x = 1.

**What these values do NOT mean:**
- High y does not predict failure
- High y does not indicate instability or criticality
- The y scale has no universal physical meaning across systems

---

## When NOT to use this package

Do not use this package if you need to:

- **Infer capacity or load** from observed data (you must supply p1 and p2 explicitly)
- **Predict when** a system will fail (this is a diagnostic, not a forecast)
- **Model dynamics** of how a system evolves over time
- **Detect phase transitions** or critical phenomena (no such claims are made)
- **Apply to systems** where the relationship between p1 and p2 is not well-defined

If you are unsure whether p1 and p2 are appropriate for your system, do not use this tool.

---

## Required Validation Steps

Before applying this diagnostic to any system, you MUST:

1. **Verify system class**: Confirm the system is finite and failure is absorbing
2. **Define p₁ independently**: p₁ must be known from external specification or measurement, never inferred from failure observations
3. **Define p₂ independently**: p₂ must be measured directly, not derived from y or outcomes
4. **Document units**: p₁ and p₂ must have consistent, documented units
5. **Run sensitivity analysis**: Use `sensitivity_check()` to assess measurement uncertainty impact
6. **Examine negative controls**: Use `negative_control_plot()` to compare against shuffled baseline

**If any step fails or is unclear, do not use this diagnostic.**

### Validation Failure is a Valid Outcome

If validation reveals that:
- Small perturbations in p₁ or p₂ produce large changes in y
- The relationship between y and outcomes is similar to shuffled controls
- Confidence intervals span most of the y range

...then **the diagnostic may not be informative for your system**. This is a valid result. Do not force interpretation when validation fails.

---

## Failure Cases

The diagnostic produces **misleading or inappropriate results** when:

| Case | Problem | Solution |
|------|---------|----------|
| p₁ estimated from same data as y | Circular reasoning | Use independently measured/specified p₁ |
| System can recover spontaneously | Absorbing-failure assumption violated | Do not use this diagnostic |
| p₁ varies over observation period | x becomes undefined | Use time-windowed p₁ or stratify |
| p₂ derived from failure counts | Survival bias contaminates measurement | Measure p₂ from operating load |
| σ(x) ≈ (1-x) | Diagnostic dominated by noise | Report uncertainty; do not over-interpret |
| System has no fixed capacity | p₁ is undefined | Do not use this diagnostic |

---

## Validation Utilities

The package includes diagnostic utilities (not correctness tests):

```python
from yp_diagnostic.validation import collapse_test, sensitivity_check

# These report diagnostics; they do not determine correctness
results = sensitivity_check(p1_values, p2_values)
```

See `docs/checklist.md` for a reproducibility checklist.

---

## Documentation

- `docs/scope.md` - Full scope and assumptions
- `docs/how_not_to_use.md` - Misuse cases and warnings
- `docs/checklist.md` - Reproducibility checklist

---

## Citation

If you use this package, please cite:

```
@software{yp_diagnostic,
  author = {Harold, Faisal},
  title = {A Diagnostic Coordinate for Finite Systems Near Capacity Thresholds},
  version = {1.0.0},
  year = {2025},
  url = {https://github.com/faisalharold/yp-diagnostic}
}
```

---

## License

MIT License. See LICENSE file.

---

## Changelog

See CHANGELOG.md for version history.

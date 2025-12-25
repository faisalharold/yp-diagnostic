# yp-diagnostic

A diagnostic coordinate for finite systems near capacity thresholds.

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

- **y increases** as x approaches 1
- **y diverges** as x -> 1
- This **flags** a regime where small changes in x produce large changes in y

**What this indicates:** The system is near a threshold where rate-based metrics may become unreliable.

**What this does NOT indicate:** Causation, prediction of failure, mechanism of transition, or universality of behavior.

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

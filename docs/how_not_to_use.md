# How NOT to Use This Package

This document describes common misuse cases and inappropriate applications of the `yp-diagnostic` package.

---

## Misuse Case 1: Inferring p1 or p2 from Data

**What users might try:**
```python
# WRONG: Trying to estimate capacity from observations
p1_estimated = max(observed_loads)  # This is not what p1 means
```

**Why this is wrong:**
- p1 must be a known, externally defined reference value
- Estimating p1 from the same data used to compute y creates circular reasoning
- The package provides no inference methods and does not validate inferred values

**What to do instead:**
- Use independently measured or specified values for p1
- If p1 is unknown, this package is not appropriate for your use case

---

## Misuse Case 2: Predicting System Failure

**What users might try:**
```python
# WRONG: Using y as a failure predictor
if y > threshold:
    alert("System will fail soon!")  # This is not a valid prediction
```

**Why this is wrong:**
- y indicates proximity to x = 1; it does not predict failure
- High y does not mean failure is imminent or inevitable
- The relationship between y and actual outcomes must be established empirically, outside this package

**What to do instead:**
- Use y as one input among many in a decision framework
- Validate any thresholds empirically with domain-specific data
- Do not claim prediction capability based on y alone

---

## Misuse Case 3: Claiming Universal Applicability

**What users might try:**
```
"The y(p) diagnostic reveals a universal law governing system collapse."
```

**Why this is wrong:**
- y(p) is a specific mathematical transformation, not a discovered law
- The (1-x)^(-1/2) function was chosen, not discovered
- Applicability to any specific domain must be validated independently

**What to do instead:**
- Describe y(p) as a "diagnostic coordinate" or "transformed ratio"
- Avoid terms like "universal," "fundamental," or "law"
- Acknowledge that the transformation is a modeling choice

---

## Misuse Case 4: Detecting Phase Transitions

**What users might try:**
```
"The divergence of y indicates a critical phase transition."
```

**Why this is wrong:**
- y diverges because of the (1-x)^(-1/2) function, not because of system physics
- The divergence is a property of the transformation, not an empirical discovery
- No claims about criticality, phase transitions, or emergent behavior are warranted

**What to do instead:**
- Describe the behavior as "y increases as x approaches 1"
- Avoid terminology from statistical physics unless independently justified
- Do not conflate mathematical properties with physical phenomena

---

## Misuse Case 5: Omitting Required Metadata

**What users might try:**
```python
# WRONG: Using placeholder metadata
x, y = compute_x_y(
    p1=100, p2=85,
    p1_name="capacity",      # Too vague
    p2_name="load",          # Too vague
    failure_definition="bad" # Meaningless
)
```

**Why this is wrong:**
- Vague metadata defeats the purpose of the guardrails
- Future users (including yourself) cannot interpret the results
- Reproducibility requires explicit semantic context

**What to do instead:**
```python
# CORRECT: Explicit, meaningful metadata
x, y = compute_x_y(
    p1=100, p2=85,
    p1_name="server_max_requests_per_second",
    p2_name="current_request_rate_per_second",
    failure_definition="p99_latency_exceeds_500ms"
)
```

---

## Misuse Case 6: Ignoring Warnings

**What users might try:**
```python
import warnings
warnings.filterwarnings("ignore")  # WRONG: Hiding important information
```

**Why this is wrong:**
- Warnings indicate that x is approaching or exceeding 1
- Ignoring warnings may hide numerical issues or inappropriate inputs
- The warnings are part of the diagnostic output

**What to do instead:**
- Read and understand all warnings
- If warnings are expected, document why
- Never silently suppress warnings in production code

---

## Misuse Case 7: Using for Dynamic Modeling

**What users might try:**
```python
# WRONG: Treating y as a dynamic variable
dy_dt = some_function(y)  # This package does not model dynamics
```

**Why this is wrong:**
- This package computes static diagnostic coordinates
- No temporal modeling, differential equations, or dynamics are supported
- y is computed pointwise, not as a trajectory

**What to do instead:**
- Use this package for snapshot diagnostics only
- For dynamic modeling, use appropriate simulation tools
- Do not extend the package beyond its stated scope

---

## Misuse Case 8: Interpreting Collapse Plots as Discovery

**What users might try:**
```
"Different systems collapse onto the same curve, revealing a universal scaling law."
```

**Why this is wrong:**
- The collapse occurs because y is defined as a function of x = p2/p1
- The overlap is definitional, not empirical
- No "discovery" is made by observing this overlap

**What to do instead:**
- Describe collapse plots as showing "consistent behavior under the transformation"
- Acknowledge that the transformation was chosen, not discovered
- Do not claim empirical discovery from mathematical properties

---

## Misuse Case 9: Using Negative Controls as Hypothesis Tests

**What users might try:**
```python
# WRONG: Treating negative controls as a statistical test
if real_y > max(shuffled_y):
    print("Statistically significant!")  # No p-value was computed
```

**Why this is wrong:**
- `negative_control_plot` generates shuffled data for visual comparison
- No hypothesis test is performed
- No p-values, confidence levels, or significance determinations are provided

**What to do instead:**
- Use negative controls for exploratory visualization only
- If statistical testing is needed, use appropriate statistical methods
- Do not claim significance without proper hypothesis testing

---

## Misuse Case 10: Extending the Package

**What users might try:**
```python
# WRONG: Adding new functionality without understanding scope
def predict_failure_time(y):
    """Predict when failure will occur based on y."""
    return some_prediction  # This violates the package scope
```

**Why this is wrong:**
- Extensions may violate the carefully defined scope
- Adding prediction, inference, or modeling contradicts the package design
- Users may conflate extensions with original package claims

**What to do instead:**
- Keep extensions in separate packages with separate documentation
- Clearly distinguish extended functionality from original package
- Do not claim that extensions are part of or endorsed by this package

---

## Summary

This package is intentionally narrow in scope. If you find yourself wanting to:

- Infer values
- Make predictions
- Claim universality
- Detect phase transitions
- Model dynamics

...then this package is not appropriate for your use case.

The `yp-diagnostic` package computes a diagnostic coordinate. That is all it does.

# Repository Review: yp-diagnostic

**Review Date:** 2025-12-30
**Reviewer:** Claude Code
**Scope:** Diagnostic coordinate y(p) = (1 - p₂/p₁)^(-1/2)

---

## Executive Summary

This repository implements a **diagnostic reparameterization** for identifying when rate-based statistical summaries may become unreliable due to proximity to capacity thresholds. The current documentation is **exceptionally well-constructed** for a methods repository, with comprehensive guardrails against misuse. This review identifies remaining gaps and recommends targeted improvements.

**Overall Assessment:** The repository demonstrates responsible design. The issues identified below are refinements, not fundamental problems.

---

## 1. README Structure Review

### Current State: Good

The existing README correctly:
- States what y(p) is (diagnostic coordinate) and is not (prediction, model, universal law)
- Limits scope through explicit "does/does not" sections
- Avoids claims of causation, dynamics, instability, or critical phenomena
- Enforces metadata requirements as guardrails
- Includes a "When NOT to use" section

### Recommended Revisions

#### 1.1 Add Explicit System Requirements Section

**Currently missing:** Explicit statement that the diagnostic applies only to:
- Finite systems
- Systems where failure is absorbing (non-reversible)

**Recommended addition after the Scope section:**

```markdown
## System Requirements

This diagnostic is designed for systems where:

1. **The system is finite**: There exists a meaningful capacity or threshold (p₁)
2. **Failure is absorbing**: Once failure occurs, the system does not spontaneously recover
3. **p₁ and p₂ are externally defined**: Values are measured or specified, not inferred

**Do not use this diagnostic for:**
- Reversible systems (where load can decrease and recovery is automatic)
- Infinite or unbounded systems (where no capacity threshold exists)
- Systems where p₁ or p₂ must be estimated from observed failures
```

#### 1.2 Strengthen "What y(p) Is NOT" Section

**Current language is good but could be more prominent.** Recommend adding a boxed warning:

```markdown
> ⚠️ **CRITICAL LIMITATION**
>
> y(p) is a **diagnostic coordinate**, not a physical law or predictive model.
>
> - The (1-x)^(-1/2) form was **chosen** for mathematical convenience, not discovered empirically
> - The divergence as x→1 is a property of **the transformation**, not the system
> - High y values indicate proximity to x=1, nothing more
```

#### 1.3 Add Interpretation Table

**Purpose:** Make y-value interpretation unambiguous.

```markdown
## Interpretation Guide

| x = p₂/p₁ | y = (1-x)^(-1/2) | Interpretation |
|-----------|------------------|----------------|
| 0.00 | 1.00 | Ratio is zero; no proximity to threshold |
| 0.50 | 1.41 | Half capacity; low x regime |
| 0.80 | 2.24 | 80% capacity; moderate x regime |
| 0.90 | 3.16 | 90% capacity; high x regime, warnings issued |
| 0.95 | 4.47 | 95% capacity; high x regime |
| 0.99 | 10.0 | 99% capacity; near-threshold |
| ≥1.00 | clipped | At/beyond threshold; clipped to ~1000 |

**What these values mean:** y quantifies how close x is to 1. Higher y = closer to x=1.

**What these values do NOT mean:**
- High y does not predict failure
- High y does not indicate instability
- The y scale has no universal meaning
```

#### 1.4 Add "Required Validation Before Use" Section

```markdown
## Required Validation Steps

Before applying this diagnostic to any system, you MUST:

1. **Verify system class**: Confirm the system is finite and failure is absorbing
2. **Define p₁ independently**: p₁ must be known from external specification or measurement, never inferred from failure observations
3. **Define p₂ independently**: p₂ must be measured directly, not derived from y
4. **Document units**: p₁ and p₂ must have consistent, documented units
5. **Run sensitivity analysis**: Use `sensitivity_check()` to assess measurement uncertainty impact
6. **Examine negative controls**: Use `negative_control_plot()` to compare against shuffled baseline

**If any step fails or is unclear, do not use this diagnostic.**
```

#### 1.5 Add Clear Failure Cases Section

```markdown
## Failure Cases (When the Diagnostic Produces Misleading Results)

The diagnostic is **inappropriate or unreliable** when:

1. **p₁ is estimated from the same data used to compute y**
   - Circular reasoning makes y meaningless
   - Solution: Use independently measured or specified p₁

2. **The system can recover spontaneously**
   - Reversible systems violate the absorbing-failure assumption
   - Solution: Do not use this diagnostic

3. **p₁ varies over the observation period**
   - Non-stationary capacity makes x undefined
   - Solution: Use time-windowed p₁ or stratify analysis

4. **p₂ is derived from failure counts**
   - Survival bias contaminates p₂ measurement
   - Solution: Measure p₂ from operating load, not outcomes

5. **Measurement uncertainty is large relative to (1-x)**
   - When σ(x) ≈ (1-x), y is dominated by noise
   - Solution: Report uncertainty and do not over-interpret
```

---

## 2. Reusability Assessment

### 2.1 Missing Information for Safe Reuse

| Gap | Risk | Recommendation |
|-----|------|----------------|
| No explicit finite/absorbing requirement in README | Users may apply to inappropriate systems | Add "System Requirements" section |
| No worked example showing validation failure | Users may not recognize when validation fails | Add synthetic example that deliberately fails |
| No guidance on minimum sample size | Users may use with insufficient data | Add note that this is user's responsibility |
| Uncertainty module lacks warning for high-x regime | Delta method accuracy degrades | Add warning when x > 0.9 in `delta_method_ci` |
| No explicit statement that y is monotonic | Users may not understand that y order = x order | Document in README |

### 2.2 Potential Misinterpretation Points

**Risk 1: Interpreting y as a "score" or "risk indicator"**
- Current mitigation: Good documentation
- Remaining gap: No runtime warning when y > some threshold
- Recommendation: Consider adding a UserWarning for y > 10 stating "High y indicates proximity to x=1 only"

**Risk 2: Believing collapse plots reveal empirical regularities**
- Current mitigation: `how_not_to_use.md` covers this
- Remaining gap: The `collapse_test` function name may imply discovery
- Recommendation: Rename to `collapse_diagnostic` or add more explicit docstring

**Risk 3: Using negative controls as hypothesis tests**
- Current mitigation: Documentation is clear
- Remaining gap: Function returns data that looks like test output
- Recommendation: Return dict should include explicit `"is_hypothesis_test": False` field

### 2.3 Additional Guardrails Needed

1. **Add validation flag to output dictionaries**
   - Include `"validated": False` in all function returns
   - Force users to explicitly acknowledge they have validated assumptions

2. **Add metadata to output**
   - Functions like `sensitivity_check` should return the input metadata (p1_name, p2_name) if provided
   - This supports traceability

3. **Add version stamp to outputs**
   - Include `"package_version": "1.0.0"` in all returned dictionaries
   - Supports reproducibility

---

## 3. Required Disclaimers and Guardrails

### 3.1 Recommended Disclaimer Language

**For README header:**
```markdown
> **DISCLAIMER**: This is a diagnostic tool, not a predictive model.
> The coordinate y(p) = (1-x)^(-1/2) is a mathematical reparameterization
> chosen for its divergent behavior near x=1. It does not:
> - Predict system failure
> - Explain system dynamics
> - Apply universally to all systems
> - Detect critical phenomena or phase transitions
>
> Any use beyond diagnostic flagging requires independent validation.
```

**For all function docstrings (already present, but strengthen):**
```
INTERPRETATION WARNING:
    This function computes a DIAGNOSTIC coordinate only.
    - It does NOT predict system behavior
    - It does NOT validate theoretical claims
    - It does NOT apply to reversible or infinite systems

    The user is responsible for verifying that:
    1. The system is finite
    2. Failure is absorbing
    3. p₁ and p₂ are independently defined
```

### 3.2 Guardrails Against Causal/Predictive Interpretation

**Current state:** Good. Required metadata enforces semantic context.

**Recommended additions:**

1. In `core.py`, add to the function return:
```python
# Consider returning a diagnostic result object instead of tuple
# that includes interpretation warnings
```

2. Add a module-level constant:
```python
DIAGNOSTIC_ONLY_WARNING = (
    "y(p) is a diagnostic coordinate indicating proximity to x=1. "
    "It does not predict failure, explain mechanisms, or apply universally."
)
```

### 3.3 Guardrails Against Use in Reversible/Infinite Systems

**Currently missing explicit check.**

The metadata requirement (`failure_definition`) partially addresses this, but a user could provide a failure definition for a reversible system.

**Recommendation:** Add to documentation a clear statement that the diagnostic is not appropriate for:
- Queuing systems with unlimited buffers (infinite)
- Elastic systems that scale automatically (no fixed p₁)
- Systems where "failure" is temporary (reversible)

### 3.4 Uncertainty Propagation Requirements

**Current state:** Bootstrap and delta method are provided with appropriate warnings.

**Recommended additions:**

1. Add explicit requirement in README:
```markdown
## Uncertainty Requirements

When reporting y(p), you SHOULD:
- Provide confidence intervals using `bootstrap_ci` or `delta_method_ci`
- Report sensitivity using `sensitivity_check`
- Document the source and magnitude of measurement uncertainty in p₁ and p₂

When reporting y(p), you MUST NOT:
- Report point estimates without uncertainty
- Interpret confidence intervals as prediction intervals
- Ignore warnings about high-x regime accuracy
```

2. Add warning to `delta_method_ci` when x > 0.9:
```python
if x > 0.9:
    warnings.warn(
        "Delta method accuracy degrades as x approaches 1. "
        "Consider using bootstrap_ci for more reliable intervals.",
        UserWarning,
        stacklevel=2
    )
```

### 3.5 Validation Failure as Valid Outcome

**Add to documentation:**
```markdown
## Validation Failure is a Valid Outcome

If sensitivity analysis reveals that:
- Small perturbations in p₁ or p₂ produce large changes in y
- The relationship between y and outcomes is similar to shuffled controls
- Confidence intervals span most of the y range

...then **the diagnostic may not be informative for your system**.

This is a valid result. It means:
- The system may not be well-characterized by the p₁/p₂ ratio
- Measurement uncertainty may be too large
- The diagnostic coordinate does not provide additional information

**Do not force interpretation when validation fails.**
```

---

## 4. API/Code Interface Review

### 4.1 Function Signature Improvements

**Current `compute_x_y` signature:** Good. Required metadata is enforced.

**Recommended additions:**

```python
def compute_x_y(
    p1: Union[float, np.ndarray],
    p2: Union[float, np.ndarray],
    p1_name: str,
    p2_name: str,
    failure_definition: str,
    # NEW: Optional parameters to reinforce diagnostic status
    acknowledge_diagnostic_only: bool = True,  # Require explicit acknowledgment
    system_is_finite: bool = True,  # Explicit statement
    failure_is_absorbing: bool = True,  # Explicit statement
) -> DiagnosticResult:  # Consider returning object instead of tuple
```

This is **optional** - the current signature is already good. The tradeoff is usability vs. explicit acknowledgment.

### 4.2 Naming Convention Recommendations

| Current | Status | Recommendation |
|---------|--------|----------------|
| `compute_x_y` | Good | Clear and neutral |
| `collapse_test` | Risky | Rename to `collapse_comparison` or `multi_dataset_diagnostic` |
| `negative_control_plot` | Good | Name clearly indicates purpose |
| `sensitivity_check` | Good | Neutral diagnostic language |
| `bootstrap_ci` | Good | Standard statistical terminology |
| `delta_method_ci` | Good | Standard statistical terminology |

### 4.3 Recommended Code Checks/Warnings

**In `core.py:compute_x_y`:**

| Check | Status | Recommendation |
|-------|--------|----------------|
| p1 > 0 | ✅ Present | — |
| p2 >= 0 | ✅ Present | — |
| x >= 0.9 warning | ✅ Present | — |
| x >= 1.0 warning | ✅ Present | — |
| Missing metadata | ✅ Present | — |
| Whitespace-only metadata | ✅ Present | — |

**Missing but recommended:**

1. **Warn if y > 10** (optional, low priority):
```python
if np.any(y > 10):
    warnings.warn(
        f"y > 10 detected. This indicates x > 0.99 (within 1% of threshold). "
        f"Interpretation: diagnostic coordinate is in high-sensitivity regime. "
        f"This is NOT a prediction of imminent failure.",
        UserWarning,
        stacklevel=2,
    )
```

2. **In `delta_method_ci`, warn when x > 0.9:**
```python
if x > 0.9:
    warnings.warn(
        "x > 0.9: Delta method approximation accuracy degrades in high-x regime. "
        "Consider using bootstrap_ci for more robust uncertainty estimates.",
        UserWarning,
        stacklevel=2,
    )
```

3. **In `bootstrap_ci`, add sample size check:**
```python
if n_boot < 1000:
    warnings.warn(
        f"n_boot={n_boot} may be insufficient for stable confidence intervals. "
        f"Consider n_boot >= 2000 for reliable estimates.",
        UserWarning,
        stacklevel=2,
    )
```

### 4.4 Output Structure Recommendations

**Current:** Functions return dictionaries.

**Recommended enhancements:**

```python
# Add to all returned dictionaries:
{
    # ... existing fields ...
    "_metadata": {
        "package_version": "1.0.0",
        "is_diagnostic_only": True,
        "is_prediction": False,
        "is_hypothesis_test": False,
    }
}
```

This makes the diagnostic-only nature programmatically accessible.

---

## 5. Final Check

### 5.1 Conditions Under Which Users Should NOT Use This Repository

1. **The system is reversible or self-healing**
   - If failures can resolve spontaneously, the absorbing-failure assumption is violated

2. **The system is infinite or unbounded**
   - If no capacity threshold exists, p₁ is undefined

3. **p₁ must be estimated from failure observations**
   - This creates circular reasoning that invalidates the diagnostic

4. **The goal is prediction**
   - This is a diagnostic, not a predictive model

5. **The user wants to claim universality**
   - The (1-x)^(-1/2) transformation has no special status

6. **Measurement uncertainty is comparable to (1-x)**
   - The diagnostic becomes noise-dominated

### 5.2 What Constitutes Misuse

| Misuse | Why It's Wrong |
|--------|----------------|
| Claiming y predicts failure | y indicates proximity, not outcome |
| Claiming universal scaling | The transformation was chosen, not discovered |
| Inferring p₁ from y | Circular reasoning |
| Interpreting collapse as discovery | Collapse is definitional |
| Suppressing warnings | Warnings contain diagnostic information |
| Using for reversible systems | Violates absorbing-failure assumption |
| Treating negative controls as p-values | No hypothesis test is performed |
| Claiming mechanism or causation | y is descriptive only |

### 5.3 Minimal Documentation for Ethical Reuse

The following **must remain visible** in any distribution:

1. **Scope limitations** (what y does and does not do)
2. **Required assumptions** (finite system, absorbing failure)
3. **Required metadata** (p1_name, p2_name, failure_definition)
4. **Interpretation warnings** (diagnostic only, not predictive)
5. **Misuse cases** (at minimum, the summary from `how_not_to_use.md`)

If any of these are removed, the repository becomes ethically problematic.

---

## Summary of Recommended Changes

### High Priority (Should Implement)

1. Add "System Requirements" section to README stating finite/absorbing requirements
2. Add interpretation table with y values
3. Add "Failure Cases" section listing when diagnostic is inappropriate
4. Add delta method warning for x > 0.9

### Medium Priority (Recommended)

5. Add validation failure documentation (failure is a valid outcome)
6. Rename `collapse_test` to `collapse_comparison` or similar
7. Add package version to returned dictionaries
8. Add explicit statement that y is monotonic in README

### Low Priority (Optional Enhancements)

9. Add warning for y > 10
10. Add bootstrap sample size warning
11. Consider returning diagnostic objects instead of tuples
12. Add `"is_hypothesis_test": False` to negative control output

---

## Conclusion

This repository is **well-designed for its stated purpose**. The documentation is comprehensive, the guardrails are thoughtfully implemented, and the scope is appropriately narrow. The recommendations above are refinements to further reduce misuse risk, not corrections to fundamental problems.

The repository demonstrates how a methods tool should be documented: with explicit scope, clear limitations, and required context. This is a model for responsible diagnostic tool design.

"""
Tests for yp_diagnostic.core module.

These tests verify:
- Correct computation of x and y
- Input validation and error handling
- Warning generation for threshold conditions
- Numerical stability near x = 1
- Metadata enforcement
"""

import numpy as np
import pytest

from yp_diagnostic.core import compute_x_y


class TestComputeXY:
    """Tests for the compute_x_y function."""

    # Required metadata for all tests
    METADATA = {
        "p1_name": "test_capacity",
        "p2_name": "test_load",
        "failure_definition": "test_failure",
    }

    def test_basic_computation(self):
        """Test basic x and y computation with valid inputs."""
        x, y = compute_x_y(p1=100.0, p2=50.0, **self.METADATA)

        assert x == pytest.approx(0.5)
        # y = (1 - 0.5)^(-0.5) = 0.5^(-0.5) = sqrt(2) ≈ 1.414
        assert y == pytest.approx(np.sqrt(2))

    def test_computation_at_zero_load(self):
        """Test computation when p2 = 0 (zero load)."""
        x, y = compute_x_y(p1=100.0, p2=0.0, **self.METADATA)

        assert x == pytest.approx(0.0)
        # y = (1 - 0)^(-0.5) = 1
        assert y == pytest.approx(1.0)

    def test_computation_with_arrays(self):
        """Test computation with numpy array inputs."""
        p1 = np.array([100.0, 100.0, 100.0])
        p2 = np.array([25.0, 50.0, 75.0])

        x, y = compute_x_y(p1=p1, p2=p2, **self.METADATA)

        expected_x = np.array([0.25, 0.5, 0.75])
        expected_y = np.power(1.0 - expected_x, -0.5)

        np.testing.assert_array_almost_equal(x, expected_x)
        np.testing.assert_array_almost_equal(y, expected_y)


class TestMetadataEnforcement:
    """Tests for required metadata validation."""

    def test_missing_p1_name_raises_error(self):
        """Verify ValueError when p1_name is missing."""
        with pytest.raises(ValueError, match="p1_name is required"):
            compute_x_y(
                p1=100.0,
                p2=50.0,
                p1_name="",
                p2_name="load",
                failure_definition="failure",
            )

    def test_missing_p2_name_raises_error(self):
        """Verify ValueError when p2_name is missing."""
        with pytest.raises(ValueError, match="p2_name is required"):
            compute_x_y(
                p1=100.0,
                p2=50.0,
                p1_name="capacity",
                p2_name="",
                failure_definition="failure",
            )

    def test_missing_failure_definition_raises_error(self):
        """Verify ValueError when failure_definition is missing."""
        with pytest.raises(ValueError, match="failure_definition is required"):
            compute_x_y(
                p1=100.0,
                p2=50.0,
                p1_name="capacity",
                p2_name="load",
                failure_definition="",
            )

    def test_whitespace_only_metadata_raises_error(self):
        """Verify ValueError when metadata is whitespace only."""
        with pytest.raises(ValueError, match="p1_name is required"):
            compute_x_y(
                p1=100.0,
                p2=50.0,
                p1_name="   ",
                p2_name="load",
                failure_definition="failure",
            )

    def test_none_metadata_raises_error(self):
        """Verify ValueError when metadata is None."""
        with pytest.raises(ValueError, match="p1_name is required"):
            compute_x_y(
                p1=100.0,
                p2=50.0,
                p1_name=None,
                p2_name="load",
                failure_definition="failure",
            )


class TestInputValidation:
    """Tests for numerical input validation."""

    METADATA = {
        "p1_name": "test_capacity",
        "p2_name": "test_load",
        "failure_definition": "test_failure",
    }

    def test_zero_p1_raises_error(self):
        """Verify ValueError when p1 = 0."""
        with pytest.raises(ValueError, match="p1 must be positive"):
            compute_x_y(p1=0.0, p2=50.0, **self.METADATA)

    def test_negative_p1_raises_error(self):
        """Verify ValueError when p1 < 0."""
        with pytest.raises(ValueError, match="p1 must be positive"):
            compute_x_y(p1=-100.0, p2=50.0, **self.METADATA)

    def test_negative_p2_raises_error(self):
        """Verify ValueError when p2 < 0."""
        with pytest.raises(ValueError, match="p2 must be non-negative"):
            compute_x_y(p1=100.0, p2=-10.0, **self.METADATA)

    def test_array_with_invalid_p1_raises_error(self):
        """Verify ValueError when any element of p1 array is non-positive."""
        p1 = np.array([100.0, 0.0, 100.0])
        p2 = np.array([50.0, 50.0, 50.0])

        with pytest.raises(ValueError, match="p1 must be positive"):
            compute_x_y(p1=p1, p2=p2, **self.METADATA)

    def test_array_with_invalid_p2_raises_error(self):
        """Verify ValueError when any element of p2 array is negative."""
        p1 = np.array([100.0, 100.0, 100.0])
        p2 = np.array([50.0, -10.0, 50.0])

        with pytest.raises(ValueError, match="p2 must be non-negative"):
            compute_x_y(p1=p1, p2=p2, **self.METADATA)


class TestWarnings:
    """Tests for warning generation."""

    METADATA = {
        "p1_name": "test_capacity",
        "p2_name": "test_load",
        "failure_definition": "test_failure",
    }

    def test_warning_at_x_0_9(self):
        """Verify UserWarning when x >= 0.9."""
        with pytest.warns(UserWarning, match="x >= 0.9"):
            compute_x_y(p1=100.0, p2=90.0, **self.METADATA)

    def test_warning_at_x_0_95(self):
        """Verify UserWarning when x = 0.95."""
        with pytest.warns(UserWarning, match="x >= 0.9"):
            compute_x_y(p1=100.0, p2=95.0, **self.METADATA)

    def test_warning_at_x_1_0(self):
        """Verify UserWarning when x >= 1.0."""
        with pytest.warns(UserWarning, match="x >= 1.0"):
            compute_x_y(p1=100.0, p2=100.0, **self.METADATA)

    def test_warning_at_x_exceeds_1(self):
        """Verify UserWarning when x > 1.0."""
        with pytest.warns(UserWarning, match="x >= 1.0"):
            compute_x_y(p1=100.0, p2=110.0, **self.METADATA)

    def test_no_warning_below_threshold(self):
        """Verify no warning when x < 0.9."""
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            # This should not raise any warnings
            compute_x_y(p1=100.0, p2=80.0, **self.METADATA)

    def test_warning_in_array_with_some_high_values(self):
        """Verify warning when some array elements have x >= 0.9."""
        p1 = np.array([100.0, 100.0, 100.0])
        p2 = np.array([50.0, 95.0, 75.0])

        with pytest.warns(UserWarning, match="x >= 0.9"):
            compute_x_y(p1=p1, p2=p2, **self.METADATA)


class TestNumericalStability:
    """Tests for numerical stability near x = 1."""

    METADATA = {
        "p1_name": "test_capacity",
        "p2_name": "test_load",
        "failure_definition": "test_failure",
    }

    def test_clipping_at_x_equals_1(self):
        """Verify y is finite when x = 1.0 (clipping applied)."""
        with pytest.warns(UserWarning):
            x, y = compute_x_y(p1=100.0, p2=100.0, **self.METADATA)

        assert x == pytest.approx(1.0)
        assert np.isfinite(y)
        # y should be large but finite due to clipping
        assert y > 100

    def test_clipping_when_x_exceeds_1(self):
        """Verify y is finite when x > 1.0 (clipping applied)."""
        with pytest.warns(UserWarning):
            x, y = compute_x_y(p1=100.0, p2=150.0, **self.METADATA)

        assert x == pytest.approx(1.5)
        assert np.isfinite(y)

    def test_stability_near_x_0_999(self):
        """Verify numerical stability at x = 0.999."""
        with pytest.warns(UserWarning):
            x, y = compute_x_y(p1=1000.0, p2=999.0, **self.METADATA)

        assert x == pytest.approx(0.999)
        # y = (1 - 0.999)^(-0.5) = 0.001^(-0.5) ≈ 31.62
        assert y == pytest.approx(31.62, rel=0.01)
        assert np.isfinite(y)

    def test_stability_with_array_near_boundary(self):
        """Verify stability with array inputs near x = 1."""
        p1 = np.array([100.0, 100.0, 100.0])
        p2 = np.array([99.0, 99.9, 99.99])

        with pytest.warns(UserWarning):
            x, y = compute_x_y(p1=p1, p2=p2, **self.METADATA)

        assert np.all(np.isfinite(x))
        assert np.all(np.isfinite(y))
        assert np.all(y > 0)

    def test_y_increases_as_x_approaches_1(self):
        """Verify that y monotonically increases as x approaches 1."""
        x_values = [0.5, 0.7, 0.8, 0.85]
        y_values = []

        for x_val in x_values:
            _, y = compute_x_y(p1=100.0, p2=x_val * 100.0, **self.METADATA)
            y_values.append(y)

        # Verify monotonic increase
        for i in range(len(y_values) - 1):
            assert y_values[i] < y_values[i + 1]


class TestReturnTypes:
    """Tests for correct return types."""

    METADATA = {
        "p1_name": "test_capacity",
        "p2_name": "test_load",
        "failure_definition": "test_failure",
    }

    def test_scalar_inputs_return_floats(self):
        """Verify scalar inputs return float outputs."""
        x, y = compute_x_y(p1=100.0, p2=50.0, **self.METADATA)

        assert isinstance(x, float)
        assert isinstance(y, float)

    def test_array_inputs_return_arrays(self):
        """Verify array inputs return array outputs."""
        p1 = np.array([100.0, 100.0])
        p2 = np.array([50.0, 75.0])

        x, y = compute_x_y(p1=p1, p2=p2, **self.METADATA)

        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert x.shape == p1.shape
        assert y.shape == p1.shape

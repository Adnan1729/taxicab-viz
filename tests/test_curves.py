"""Tests for taxicab.curves."""

import numpy as np
import pytest

from taxicab.curves import sample_curve_full, sample_curve_positive


class TestSampleCurvePositive:
    def test_curve_lies_on_equation(self) -> None:
        n = 1729
        xs, ys = sample_curve_positive(n, n_points=100)
        residual = xs**3 + ys**3 - n
        np.testing.assert_allclose(residual, 0, atol=1e-6)

    def test_endpoints_are_axes(self) -> None:
        n = 1729
        xs, ys = sample_curve_positive(n)
        cbrt_n = n ** (1 / 3)
        # Cube-root sampling near the endpoint amplifies float error:
        # a residual of ~1e-13 in x^3 becomes ~1e-4 after cbrt. This is fine
        # for plotting — the visible endpoint is still correct — but the
        # tolerance has to reflect the cube-root sensitivity.
        assert xs[0] == 0.0
        np.testing.assert_allclose(ys[0], cbrt_n, rtol=1e-9)
        np.testing.assert_allclose(xs[-1], cbrt_n, rtol=1e-9)
        np.testing.assert_allclose(ys[-1], 0.0, atol=1e-3)

    def test_first_quadrant(self) -> None:
        xs, ys = sample_curve_positive(1729)
        assert (xs >= 0).all()
        assert (ys >= 0).all()

    def test_rejects_non_positive_n(self) -> None:
        with pytest.raises(ValueError):
            sample_curve_positive(0)
        with pytest.raises(ValueError):
            sample_curve_positive(-1)


class TestSampleCurveFull:
    def test_curve_lies_on_equation(self) -> None:
        n = 91
        xs, ys = sample_curve_full(n, x_range=(-10.0, 10.0), n_points=200)
        residual = xs**3 + ys**3 - n
        np.testing.assert_allclose(residual, 0, atol=1e-6)

    def test_asymptote_behavior(self) -> None:
        """Far from origin, y should approach -x."""
        n = 91
        xs, ys = sample_curve_full(n, x_range=(-1000.0, 1000.0), n_points=100)
        # At large |x|, y + x should approach 0.
        assert abs(ys[0] + xs[0]) < 0.01
        assert abs(ys[-1] + xs[-1]) < 0.01

    def test_rejects_invalid_range(self) -> None:
        with pytest.raises(ValueError):
            sample_curve_full(100, x_range=(5.0, 5.0))

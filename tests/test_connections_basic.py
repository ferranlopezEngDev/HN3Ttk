from __future__ import annotations

from math import isclose, log10, pi

from hn3ttk.connections import (
    CustomFactorPolynomialConnection,
    LinearInterpolationConnection,
    PipeDarcy,
    PipeFixedPowerLaw,
    PipeLocalPowerLaw,
    PolynomialRegressionConnection,
    SplineSecantExtrapolationConnection,
    SplineInterpolationConnection,
    SplineTangentExtrapolationConnection,
)


def check_connection_inverse(
    name: str,
    connection,
    q: float,
    rel_tol: float = 1.0e-6,
    abs_tol: float = 1.0e-9,
) -> None:
    """
    Basic consistency check:

        q -> delta_h -> q_inv

    For passive connections:
        q > 0       -> delta_h < 0
        delta_h < 0 -> q_inv > 0
    """
    delta_h = connection.head_loss(q)
    q_inv = connection.flow_rate(delta_h)

    print()
    print(name)
    print("q       =", q)
    print("delta_h =", delta_h)
    print("q_inv   =", q_inv)
    print("dH/dQ   =", connection.head_loss_derivative(q))
    print("dQ/dH   =", connection.flow_rate_derivative(delta_h))

    assert delta_h < 0.0
    assert q_inv > 0.0
    assert isclose(q_inv, q, rel_tol=rel_tol, abs_tol=abs_tol)

    assert connection.head_loss_derivative(q) < 0.0
    assert connection.flow_rate_derivative(delta_h) < 0.0


def flow_rate_from_reynolds(
    reynolds: float,
    diameter: float = 0.05,
    kinematic_viscosity: float = 1.0e-6,
) -> float:
    return reynolds * pi * diameter * kinematic_viscosity / 4.0


def linear_interpolate(
    x: float,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
) -> float:
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def test_pipe_fixed_power_law() -> None:
    connection = PipeFixedPowerLaw(
        parameters={
            "k": 120.0,
            "n": 2.0,
        }
    )

    check_connection_inverse(
        name="PipeFixedPowerLaw",
        connection=connection,
        q=0.1,
    )


def test_pipe_fixed_power_law_jacobian_derivative_modes() -> None:
    connection = PipeFixedPowerLaw(
        parameters={
            "k": 100.0,
            "n": 2.0,
        }
    )

    assert connection.jacobian_derivative(-5.0, method="normal") < 0.0
    assert connection.jacobian_derivative(-5.0, method="tendency") < 0.0
    assert (
        connection.jacobian_derivative(
            -5.0,
            method="inverse_head_loss",
        )
        < 0.0
    )
    assert (
        connection.jacobian_derivative(
            -5.0,
            method="finite_difference",
        )
        < 0.0
    )

    connection.set_jacobian_derivative_mode("tendency")

    assert connection.get_jacobian_derivative_mode() == "tendency"
    assert isclose(
        connection.jacobian_derivative(-5.0, method="default"),
        connection.jacobian_derivative(-5.0, method="tendency"),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    try:
        connection.set_jacobian_derivative_mode("invalid_mode")
    except ValueError as error:
        assert "Invalid jacobian derivative mode" in str(error)
    else:
        raise AssertionError("Expected ValueError for invalid mode.")


def test_connection_plot_helpers() -> None:
    connection = PipeFixedPowerLaw(
        parameters={
            "k": 120.0,
            "n": 2.0,
        }
    )

    head_plot = connection.head_loss_plot_data(
        q_start=-0.1,
        q_end=0.1,
        n=5,
    )
    expected_flow_rates = [-0.1, -0.05, 0.0, 0.05, 0.1]
    assert len(head_plot["flow_rates"]) == len(expected_flow_rates)
    for value, expected_value in zip(
        head_plot["flow_rates"],
        expected_flow_rates,
    ):
        assert isclose(
            value,
            expected_value,
            rel_tol=1.0e-12,
            abs_tol=1.0e-12,
        )
    assert len(head_plot["head_losses"]) == 5
    assert len(head_plot["derivatives"]) == 5
    assert len(head_plot["tendencies"]) == 5
    assert isclose(
        head_plot["head_losses"][0],
        connection.head_loss(-0.1),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        head_plot["derivatives"][-1],
        connection.head_loss_derivative(0.1),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    flow_plot = connection.flow_rate_plot_data(
        delta_h_start=1.2,
        delta_h_end=-1.2,
        n=5,
    )
    expected_head_losses = [1.2, 0.6, 0.0, -0.6, -1.2]
    assert len(flow_plot["head_losses"]) == len(expected_head_losses)
    for value, expected_value in zip(
        flow_plot["head_losses"],
        expected_head_losses,
    ):
        assert isclose(
            value,
            expected_value,
            rel_tol=1.0e-12,
            abs_tol=1.0e-12,
        )
    assert len(flow_plot["flow_rates"]) == 5
    assert len(flow_plot["derivatives"]) == 5
    assert len(flow_plot["tendencies"]) == 5
    assert isclose(
        flow_plot["flow_rates"][0],
        connection.flow_rate(1.2),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        flow_plot["derivatives"][-1],
        connection.flow_rate_derivative(-1.2),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_pipe_darcy() -> None:
    connection = PipeDarcy(
        parameters={
            "length": 100.0,
            "diameter": 0.05,
            "roughness": 1.5e-4,
        }
    )

    check_connection_inverse(
        name="PipeDarcy",
        connection=connection,
        q=0.001,
        rel_tol=1.0e-5,
    )


def test_pipe_darcy_regime_boundaries() -> None:
    connection = PipeDarcy(
        parameters={
            "length": 100.0,
            "diameter": 0.05,
            "roughness": 1.5e-4,
        }
    )

    q_laminar_limit = flow_rate_from_reynolds(2000.0)
    q_transition_low = flow_rate_from_reynolds(2500.0)
    q_transition = flow_rate_from_reynolds(3000.0)
    q_transition_high = flow_rate_from_reynolds(3500.0)
    q_turbulent_limit = flow_rate_from_reynolds(4000.0)

    assert connection.flow_regime(q_laminar_limit) == "laminar"
    assert connection.flow_regime(q_transition) == "transition"
    assert connection.flow_regime(q_turbulent_limit) == "turbulent"

    assert isclose(
        connection.friction_factor_from_reynolds(2000.0),
        64.0 / 2000.0,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    expected_turbulent_factor = 0.25 / log10(
        (1.5e-4 / 0.05) / 3.7 + 5.74 / 4000.0**0.9
    ) ** 2
    assert isclose(
        connection.friction_factor_from_reynolds(4000.0),
        expected_turbulent_factor,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    head_loss_laminar_limit = abs(connection.head_loss(q_laminar_limit))
    head_loss_transition_low = abs(connection.head_loss(q_transition_low))
    head_loss_transition = abs(connection.head_loss(q_transition))
    head_loss_transition_high = abs(connection.head_loss(q_transition_high))
    head_loss_turbulent_limit = abs(connection.head_loss(q_turbulent_limit))

    assert isclose(
        head_loss_transition_low,
        linear_interpolate(
            q_transition_low,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        head_loss_transition,
        linear_interpolate(
            q_transition,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        head_loss_transition_high,
        linear_interpolate(
            q_transition_high,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_pipe_local_power_law() -> None:
    connection = PipeLocalPowerLaw(
        parameters={
            "length": 100.0,
            "diameter": 0.05,
            "roughness": 1.5e-4,
        }
    )

    check_connection_inverse(
        name="PipeLocalPowerLaw",
        connection=connection,
        q=0.001,
        rel_tol=1.0e-5,
    )


def test_pipe_local_power_law_transition_is_linear_in_q_head_plane() -> None:
    connection = PipeLocalPowerLaw(
        parameters={
            "length": 100.0,
            "diameter": 0.05,
            "roughness": 1.5e-4,
        }
    )

    q_laminar_limit = flow_rate_from_reynolds(2000.0)
    q_transition_low = flow_rate_from_reynolds(2500.0)
    q_transition = flow_rate_from_reynolds(3000.0)
    q_transition_high = flow_rate_from_reynolds(3500.0)
    q_turbulent_limit = flow_rate_from_reynolds(4000.0)

    head_loss_laminar_limit = abs(connection.head_loss(q_laminar_limit))
    head_loss_transition_low = abs(connection.head_loss(q_transition_low))
    head_loss_transition = abs(connection.head_loss(q_transition))
    head_loss_transition_high = abs(connection.head_loss(q_transition_high))
    head_loss_turbulent_limit = abs(connection.head_loss(q_turbulent_limit))

    assert isclose(
        head_loss_transition_low,
        linear_interpolate(
            q_transition_low,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        head_loss_transition,
        linear_interpolate(
            q_transition,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        head_loss_transition_high,
        linear_interpolate(
            q_transition_high,
            q_laminar_limit,
            head_loss_laminar_limit,
            q_turbulent_limit,
            head_loss_turbulent_limit,
        ),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    darcy_reference = PipeDarcy(
        parameters={
            "length": 100.0,
            "diameter": 0.05,
            "roughness": 1.5e-4,
        }
    )
    reference_transition_head_loss = abs(darcy_reference.head_loss(q_transition))
    assert isclose(
        head_loss_transition,
        reference_transition_head_loss,
        rel_tol=0.1,
        abs_tol=0.0,
    )

    k_transition, n_transition = connection.local_power_law_parameters(q_transition)
    assert k_transition > 0.0
    assert n_transition > 0.0


def test_linear_interpolation() -> None:
    connection = LinearInterpolationConnection(
        parameters={
            "flow_rates": [-0.02, 0.0, 0.02],
            "head_losses": [3.0, 0.0, -3.0],
        }
    )

    check_connection_inverse(
        name="LinearInterpolationConnection",
        connection=connection,
        q=0.01,
    )


def test_polynomial_regression() -> None:
    connection = PolynomialRegressionConnection(
        parameters={
            "flow_rates": [-0.02, 0.0, 0.02],
            "head_losses": [3.0, 0.0, -3.0],
            "degree": 1,
        }
    )

    check_connection_inverse(
        name="PolynomialRegressionConnection",
        connection=connection,
        q=0.01,
    )


def test_spline_interpolation() -> None:
    connection = SplineInterpolationConnection(
        parameters={
            "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
            "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
            "method": "pchip",
        }
    )

    check_connection_inverse(
        name="SplineInterpolationConnection",
        connection=connection,
        q=0.01,
    )


def test_spline_tangent_extrapolation() -> None:
    connection = SplineTangentExtrapolationConnection(
        parameters={
            "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
            "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
            "method": "pchip",
        }
    )

    check_connection_inverse(
        name="SplineTangentExtrapolationConnection",
        connection=connection,
        q=0.01,
    )


def test_spline_tangent_extrapolation_uses_endpoint_tangent_outside_range() -> None:
    connection = SplineTangentExtrapolationConnection(
        parameters={
            "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
            "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
            "method": "pchip",
        }
    )

    q_left = -0.03
    q_right = 0.03
    q_min = -0.02
    q_max = 0.02

    left_head = connection.head_loss(q_min)
    right_head = connection.head_loss(q_max)
    left_slope = connection.head_loss_derivative(q_min)
    right_slope = connection.head_loss_derivative(q_max)

    assert isclose(
        connection.head_loss(q_left),
        left_head + left_slope * (q_left - q_min),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss(q_right),
        right_head + right_slope * (q_right - q_max),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss_derivative(q_left),
        left_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss_derivative(q_right),
        right_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    head_min = -3.0
    head_max = 3.0
    head_left = 4.0
    head_right = -4.0
    flow_at_head_max = connection.flow_rate(head_max)
    flow_at_head_min = connection.flow_rate(head_min)
    slope_at_head_max = connection.flow_rate_derivative(head_max)
    slope_at_head_min = connection.flow_rate_derivative(head_min)

    assert isclose(
        connection.flow_rate(head_left),
        flow_at_head_max + slope_at_head_max * (head_left - head_max),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate(head_right),
        flow_at_head_min + slope_at_head_min * (head_right - head_min),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate_derivative(head_left),
        slope_at_head_max,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate_derivative(head_right),
        slope_at_head_min,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_spline_secant_extrapolation() -> None:
    connection = SplineSecantExtrapolationConnection(
        parameters={
            "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
            "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
            "method": "pchip",
        }
    )

    check_connection_inverse(
        name="SplineSecantExtrapolationConnection",
        connection=connection,
        q=0.01,
    )


def test_spline_secant_extrapolation_uses_boundary_segments_outside_range() -> None:
    connection = SplineSecantExtrapolationConnection(
        parameters={
            "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
            "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
            "method": "pchip",
        }
    )

    left_slope = (1.0 - 3.0) / (-0.01 - (-0.02))
    right_slope = (-3.0 - (-1.0)) / (0.02 - 0.01)

    assert isclose(
        connection.head_loss(-0.03),
        3.0 + left_slope * (-0.03 - (-0.02)),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss(0.03),
        -3.0 + right_slope * (0.03 - 0.02),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss_derivative(-0.03),
        left_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.head_loss_derivative(0.03),
        right_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )

    inverse_left_slope = (-0.01 - (-0.02)) / (1.0 - 3.0)
    inverse_right_slope = (0.02 - 0.01) / (-3.0 - (-1.0))

    assert isclose(
        connection.flow_rate(4.0),
        -0.02 + inverse_left_slope * (4.0 - 3.0),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate(-4.0),
        0.02 + inverse_right_slope * (-4.0 - (-3.0)),
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate_derivative(4.0),
        inverse_left_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )
    assert isclose(
        connection.flow_rate_derivative(-4.0),
        inverse_right_slope,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_custom_factor_polynomial() -> None:
    connection = CustomFactorPolynomialConnection(
        parameters={
            "coefficients": [10.0, 120.0],
            "exponents": [1.0, 2.0],
        }
    )

    check_connection_inverse(
        name="CustomFactorPolynomialConnection",
        connection=connection,
        q=0.1,
    )


if __name__ == "__main__":
    test_pipe_fixed_power_law()
    test_pipe_fixed_power_law_jacobian_derivative_modes()
    test_connection_plot_helpers()
    test_pipe_darcy()
    test_pipe_local_power_law()
    test_linear_interpolation()
    test_polynomial_regression()
    test_spline_interpolation()
    test_spline_secant_extrapolation()
    test_spline_secant_extrapolation_uses_boundary_segments_outside_range()
    test_spline_tangent_extrapolation()
    test_spline_tangent_extrapolation_uses_endpoint_tangent_outside_range()
    test_custom_factor_polynomial()

    print()
    print("All basic connection tests passed.")

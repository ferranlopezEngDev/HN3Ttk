from __future__ import annotations

from math import isclose

from hn3ttk.connections import (
    CustomFactorPolynomialConnection,
    LinearInterpolationConnection,
    PipeDarcy,
    PipeFixedPowerLaw,
    PipeLocalPowerLaw,
    PolynomialRegressionConnection,
    SplineInterpolationConnection,
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
    test_pipe_darcy()
    test_pipe_local_power_law()
    test_linear_interpolation()
    test_polynomial_regression()
    test_spline_interpolation()
    test_custom_factor_polynomial()

    print()
    print("All basic connection tests passed.")

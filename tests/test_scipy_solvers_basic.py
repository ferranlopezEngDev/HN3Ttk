from __future__ import annotations

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, ReservoirNode
from hn3ttk.solvers import (
    solve_alpha_continuation_scipy_least_squares,
    solve_alpha_continuation_scipy_root,
    solve_scipy_least_squares,
    solve_scipy_root,
)
from hn3ttk.system import HydraulicSystem


def build_single_pipe_system() -> HydraulicSystem:
    system = HydraulicSystem(id="single_pipe_scipy_solver_system")

    reservoir = ReservoirNode(
        id="reservoir",
        parameters={
            "elevation": 0.0,
            "head": 10.0,
        },
    )

    demand = DemandNode(
        id="demand",
        parameters={
            "elevation": 0.0,
            "initial_head": 5.0,
            "demand": 0.1,
        },
    )

    pipe = PipeFixedPowerLaw(
        id="pipe",
        parameters={
            "k": 100.0,
            "n": 2.0,
        },
    )

    system.add_node(reservoir)
    system.add_node(demand)
    system.add_connection(pipe)
    system.connect(
        connection_id="pipe",
        from_node_id="reservoir",
        to_node_id="demand",
        link_id="link_1",
    )

    return system


def test_scipy_root_hybr_with_jacobian() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_root(
        system,
        method="hybr",
        use_jacobian=True,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.metadata["solver"] == "scipy_root"
    assert result.metadata["scipy_method"] == "hybr"
    assert result.metadata["jacobian_used"] is True


def test_scipy_root_hybr_without_jacobian() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_root(
        system,
        method="hybr",
        use_jacobian=False,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.metadata["jacobian_used"] is False


def test_alpha_continuation_scipy_root() -> None:
    system = build_single_pipe_system()

    result = solve_alpha_continuation_scipy_root(
        system,
        method="hybr",
        use_jacobian=True,
        alpha_steps=5,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.metadata["solver"] == "alpha_continuation_scipy_root"


def test_scipy_root_lm() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_root(
        system,
        method="lm",
        use_jacobian=True,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8


def test_scipy_root_derivative_free_methods_smoke() -> None:
    system = build_single_pipe_system()
    methods = ["broyden1", "df-sane"]

    for method in methods:
        result = solve_scipy_root(
            system,
            method=method,
            use_jacobian=False,
            residual_tolerance=1.0e-7,
            max_function_evaluations=200,
        )

        assert result.success is True
        assert abs(result.unknown_heads[0] - 9.0) < 1.0e-6
        assert result.max_abs_residual < 1.0e-6


def test_scipy_least_squares_trf_with_jacobian() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_least_squares(
        system,
        method="trf",
        use_jacobian=True,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.metadata["solver"] == "scipy_least_squares"
    assert result.metadata["scipy_method"] == "trf"


def test_scipy_least_squares_trf_without_jacobian() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_least_squares(
        system,
        method="trf",
        use_jacobian=False,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8


def test_scipy_least_squares_lm() -> None:
    system = build_single_pipe_system()

    result = solve_scipy_least_squares(
        system,
        method="lm",
        use_jacobian=True,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8


def test_alpha_continuation_scipy_least_squares() -> None:
    system = build_single_pipe_system()

    result = solve_alpha_continuation_scipy_least_squares(
        system,
        method="trf",
        use_jacobian=True,
        alpha_steps=5,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.metadata["solver"] == "alpha_continuation_scipy_least_squares"


def test_invalid_methods_raise_error() -> None:
    system = build_single_pipe_system()

    try:
        solve_scipy_root(system, method="invalid")
    except ValueError as error:
        assert "Invalid SciPy root method" in str(error)
    else:
        raise AssertionError("Expected ValueError for invalid scipy root method.")

    try:
        solve_scipy_least_squares(system, method="invalid")
    except ValueError as error:
        assert "Invalid SciPy least_squares method" in str(error)
    else:
        raise AssertionError(
            "Expected ValueError for invalid scipy least_squares method."
        )


if __name__ == "__main__":
    test_scipy_root_hybr_with_jacobian()
    test_scipy_root_hybr_without_jacobian()
    test_alpha_continuation_scipy_root()
    test_scipy_root_lm()
    test_scipy_root_derivative_free_methods_smoke()
    test_scipy_least_squares_trf_with_jacobian()
    test_scipy_least_squares_trf_without_jacobian()
    test_scipy_least_squares_lm()
    test_alpha_continuation_scipy_least_squares()
    test_invalid_methods_raise_error()
    print("All basic SciPy solver tests passed.")

from __future__ import annotations

from hn3ttk.benchmarks import (
    build_hardy_cross_loop_system,
    build_medium_generic_network_system,
    build_parallel_pipes_system,
    build_single_pipe_system,
    build_three_reservoirs_system,
    compare_solvers,
    validate_medium_generic_network_result,
    validate_result_basic,
    validate_single_pipe_result,
)
from hn3ttk.solvers import (
    solve_alpha_continuation_damped_newton,
    solve_damped_newton_raphson,
    solve_newton_raphson,
    solve_scipy_least_squares,
    solve_scipy_root,
)


def test_single_pipe_benchmark_solves() -> None:
    system = build_single_pipe_system()
    result = solve_newton_raphson(system)
    validate_single_pipe_result(result)


def test_parallel_pipes_benchmark_solves_with_default_solvers() -> None:
    system = build_parallel_pipes_system()

    result_damped = solve_damped_newton_raphson(system)
    validate_result_basic(result_damped)

    result_root = solve_scipy_root(system, method="hybr")
    validate_result_basic(result_root)

    result_least_squares = solve_scipy_least_squares(system, method="trf")
    validate_result_basic(result_least_squares)


def test_three_reservoirs_benchmark_solves() -> None:
    system = build_three_reservoirs_system()

    result_damped = solve_damped_newton_raphson(system)
    validate_result_basic(result_damped)

    result_root = solve_scipy_root(system, method="hybr")
    validate_result_basic(result_root)


def test_hardy_cross_loop_benchmark_solves() -> None:
    system = build_hardy_cross_loop_system()

    result_alpha_damped = solve_alpha_continuation_damped_newton(
        system,
        alpha_steps=8,
    )
    validate_result_basic(result_alpha_damped, residual_tolerance=1.0e-7)

    result_least_squares = solve_scipy_least_squares(system, method="trf")
    validate_result_basic(result_least_squares, residual_tolerance=1.0e-7)


def test_medium_generic_network_solves() -> None:
    system = build_medium_generic_network_system()

    result_alpha_damped = solve_alpha_continuation_damped_newton(
        system,
        alpha_steps=10,
    )
    validate_medium_generic_network_result(
        result_alpha_damped,
        residual_tolerance=1.0e-7,
    )

    result_least_squares = solve_scipy_least_squares(system, method="trf")
    validate_medium_generic_network_result(
        result_least_squares,
        residual_tolerance=1.0e-7,
    )


def test_compare_solvers_returns_rows() -> None:
    rows = compare_solvers(build_single_pipe_system())

    assert len(rows) > 0

    for row in rows:
        assert "solver" in row
        assert "success" in row
        assert "message" in row
        assert "iterations" in row
        assert "max_abs_residual" in row


if __name__ == "__main__":
    test_single_pipe_benchmark_solves()
    test_parallel_pipes_benchmark_solves_with_default_solvers()
    test_three_reservoirs_benchmark_solves()
    test_hardy_cross_loop_benchmark_solves()
    test_medium_generic_network_solves()
    test_compare_solvers_returns_rows()
    print("All basic benchmark tests passed.")

from __future__ import annotations

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, ReservoirNode
from hn3ttk.solvers import (
    solve_alpha_continuation_damped_newton,
    solve_alpha_continuation_newton,
    solve_damped_newton_raphson,
    solve_newton_raphson,
)
from hn3ttk.system import HydraulicSystem


def build_single_pipe_system() -> HydraulicSystem:
    system = HydraulicSystem(id="single_pipe_solver_system")

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


def test_newton_raphson_solves_single_pipe_system() -> None:
    system = build_single_pipe_system()

    result = solve_newton_raphson(system)

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.state is not None
    assert result.metadata["solver"] == "newton_raphson"


def test_alpha_continuation_newton_solves_single_pipe_system() -> None:
    system = build_single_pipe_system()

    result = solve_alpha_continuation_newton(
        system,
        alpha_start=0.0,
        alpha_end=1.0,
        alpha_steps=5,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.state is not None
    assert result.metadata["solver"] == "alpha_continuation_newton"


def test_damped_newton_raphson_solves_single_pipe_system() -> None:
    system = build_single_pipe_system()

    result = solve_damped_newton_raphson(system)

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.state is not None
    assert result.metadata["solver"] == "damped_newton_raphson"


def test_damped_newton_raphson_damps_alpha_zero_single_pipe_system() -> None:
    system = build_single_pipe_system()

    result = solve_damped_newton_raphson(system, alpha=0.0)

    assert result.success is True
    assert abs(result.unknown_heads[0] - 10.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.state is not None
    assert result.metadata["solver"] == "damped_newton_raphson"
    assert any(
        entry.get("damping_factor", 1.0) < 1.0
        for entry in result.history
    )


def test_alpha_continuation_damped_newton_solves_single_pipe_system() -> None:
    system = build_single_pipe_system()

    result = solve_alpha_continuation_damped_newton(
        system,
        alpha_start=0.0,
        alpha_end=1.0,
        alpha_steps=5,
    )

    assert result.success is True
    assert abs(result.unknown_heads[0] - 9.0) < 1.0e-8
    assert result.max_abs_residual < 1.0e-8
    assert result.state is not None
    assert result.metadata["solver"] == "alpha_continuation_damped_newton"


def test_solver_result_to_dict() -> None:
    system = build_single_pipe_system()
    result = solve_newton_raphson(system)

    data = result.to_dict()

    assert "success" in data
    assert "message" in data
    assert "iterations" in data
    assert "unknown_heads" in data
    assert "residuals" in data
    assert "max_abs_residual" in data
    assert "state" in data
    assert "history" in data
    assert "metadata" in data


if __name__ == "__main__":
    test_newton_raphson_solves_single_pipe_system()
    test_alpha_continuation_newton_solves_single_pipe_system()
    test_damped_newton_raphson_solves_single_pipe_system()
    test_damped_newton_raphson_damps_alpha_zero_single_pipe_system()
    test_alpha_continuation_damped_newton_solves_single_pipe_system()
    test_solver_result_to_dict()
    print("All basic solver tests passed.")

from __future__ import annotations

from inspect import signature

from hn3ttk.connections import (
    PipeDarcy,
    PipeDarcyParameters,
    PipeFixedPowerLaw,
    PipeFixedPowerLawParameters,
)
from hn3ttk.nodes import (
    DemandNode,
    DemandNodeParameters,
    ReservoirNode,
    ReservoirNodeParameters,
)
from hn3ttk.solvers import (
    JacobianDerivativeMode,
    ScipyRootMethod,
    solve_newton_raphson,
    solve_scipy_root,
)


def test_class_signatures_expose_typed_parameter_dicts() -> None:
    assert "DemandNodeParameters" in str(signature(DemandNode))
    assert "ReservoirNodeParameters" in str(signature(ReservoirNode))
    assert "PipeFixedPowerLawParameters" in str(signature(PipeFixedPowerLaw))
    assert "PipeDarcyParameters" in str(signature(PipeDarcy))


def test_solver_signatures_expose_literal_option_aliases() -> None:
    assert "JacobianDerivativeMode" in str(signature(solve_newton_raphson))
    assert "ScipyRootMethod" in str(signature(solve_scipy_root))


def test_exported_editor_hint_types_work_in_regular_usage() -> None:
    derivative_mode: JacobianDerivativeMode = "finite_difference"
    root_method: ScipyRootMethod = "hybr"

    demand_parameters: DemandNodeParameters = {
        "elevation": 0.0,
        "initial_head": 5.0,
        "demand": 0.1,
    }
    reservoir_parameters: ReservoirNodeParameters = {
        "elevation": 0.0,
        "head": 10.0,
    }
    pipe_parameters: PipeFixedPowerLawParameters = {
        "k": 100.0,
        "n": 2.0,
        "jacobian_derivative": derivative_mode,
    }
    darcy_parameters: PipeDarcyParameters = {
        "length": 100.0,
        "diameter": 0.05,
        "roughness": 1.5e-4,
    }

    demand = DemandNode(parameters=demand_parameters)
    reservoir = ReservoirNode(parameters=reservoir_parameters)
    pipe = PipeFixedPowerLaw(parameters=pipe_parameters)
    darcy_pipe = PipeDarcy(parameters=darcy_parameters)

    assert demand.external_flow() == -0.1
    assert reservoir.fixed_head() == 10.0
    assert pipe.get_jacobian_derivative_mode() == derivative_mode
    assert darcy_pipe.head_loss(0.001) < 0.0
    assert root_method == "hybr"

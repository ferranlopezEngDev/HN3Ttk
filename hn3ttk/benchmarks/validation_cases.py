from __future__ import annotations

from math import isfinite
from typing import Any


def expected_single_pipe_solution() -> dict[str, Any]:
    """Return the reference analytical solution for the single-pipe case."""
    return {
        "unknown_heads": {"demand": 9.0},
        "link_flow_rates": {"link_1": 0.1},
        "link_delta_h": {"link_1": -1.0},
        "tolerance": 1.0e-8,
    }


def validate_result_basic(result: Any, residual_tolerance: float = 1.0e-8) -> None:
    """Validate generic solver success and finite hydraulic values."""
    assert result.success is True
    assert result.state is not None
    assert result.max_abs_residual <= residual_tolerance

    state = result.state

    for node_data in state["nodes"].values():
        assert isfinite(float(node_data["head"]))

    for link_data in state["links"].values():
        assert isfinite(float(link_data["flow_rate"]))
        assert isfinite(float(link_data["delta_h"]))


def validate_single_pipe_result(result: Any) -> None:
    """Validate the analytical single-pipe solution."""
    validate_result_basic(result, residual_tolerance=1.0e-8)

    state = result.state
    assert state is not None
    reference = expected_single_pipe_solution()
    tolerance = float(reference["tolerance"])

    demand_head = float(state["nodes"]["demand"]["head"])
    link_flow = float(state["links"]["link_1"]["flow_rate"])
    link_delta_h = float(state["links"]["link_1"]["delta_h"])

    assert abs(demand_head - reference["unknown_heads"]["demand"]) <= tolerance
    assert abs(link_flow - reference["link_flow_rates"]["link_1"]) <= tolerance
    assert abs(link_delta_h - reference["link_delta_h"]["link_1"]) <= tolerance
    assert result.max_abs_residual <= tolerance


def validate_medium_generic_network_result(
    result: Any,
    residual_tolerance: float = 1.0e-8,
) -> None:
    """Validate structural properties of the medium generic network."""
    validate_result_basic(result, residual_tolerance=residual_tolerance)

    state = result.state
    assert state is not None

    assert len(state["nodes"]) == 8
    assert len(state["links"]) == 11
    assert len(state["unknown_node_ids"]) == 6
    assert len(state["fixed_node_ids"]) == 2
    assert result.max_abs_residual <= residual_tolerance

    flow_rates = [
        float(link_data["flow_rate"])
        for link_data in state["links"].values()
    ]
    assert any(isfinite(flow_rate) for flow_rate in flow_rates)

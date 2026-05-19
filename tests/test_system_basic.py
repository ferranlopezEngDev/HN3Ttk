from __future__ import annotations

from math import isclose, sqrt

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, JunctionNode, ReservoirNode
from hn3ttk.system import HydraulicSystem, Link


def build_single_pipe_system() -> HydraulicSystem:
    """
    Build a simple system:

        reservoir -- pipe --> demand_node

    Link orientation:
        reservoir -> demand_node

    Therefore:
        q > 0 means flow from reservoir to demand node.
    """
    system = HydraulicSystem(id="single_pipe_system")

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


def test_link_creation() -> None:
    link = Link(
        id="link_test",
        connection_id="pipe_1",
        from_node_id="node_a",
        to_node_id="node_b",
    )

    assert link.id == "link_test"
    assert link.connection_id == "pipe_1"
    assert link.from_node_id == "node_a"
    assert link.to_node_id == "node_b"
    assert link.metadata == {}


def test_link_reversed() -> None:
    link = Link(
        id="link_test",
        connection_id="pipe_1",
        from_node_id="node_a",
        to_node_id="node_b",
        metadata={"name": "test link"},
    )

    reversed_link = link.reversed()

    assert reversed_link.connection_id == "pipe_1"
    assert reversed_link.from_node_id == "node_b"
    assert reversed_link.to_node_id == "node_a"
    assert reversed_link.metadata == {"name": "test link"}


def test_link_to_dict_and_from_dict() -> None:
    link = Link(
        id="link_test",
        connection_id="pipe_1",
        from_node_id="node_a",
        to_node_id="node_b",
        metadata={"name": "test link"},
    )

    data = link.to_dict()
    rebuilt = Link.from_dict(data)

    assert rebuilt.id == "link_test"
    assert rebuilt.connection_id == "pipe_1"
    assert rebuilt.from_node_id == "node_a"
    assert rebuilt.to_node_id == "node_b"
    assert rebuilt.metadata["name"] == "test link"


def test_system_add_objects() -> None:
    system = HydraulicSystem(id="test_system")

    reservoir = ReservoirNode(
        id="reservoir",
        parameters={
            "elevation": 0.0,
            "head": 10.0,
        },
    )

    junction = JunctionNode(
        id="junction",
        parameters={
            "elevation": 0.0,
            "initial_head": 5.0,
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
    system.add_node(junction)
    system.add_connection(pipe)

    link = system.connect(
        connection_id="pipe",
        from_node_id="reservoir",
        to_node_id="junction",
        link_id="link_1",
    )

    assert system.get_node("reservoir") is reservoir
    assert system.get_node("junction") is junction
    assert system.get_connection("pipe") is pipe
    assert system.get_link("link_1") is link

    assert len(system.nodes) == 2
    assert len(system.connections) == 1
    assert len(system.links) == 1


def test_fixed_and_unknown_node_ids() -> None:
    system = build_single_pipe_system()

    assert system.fixed_head_node_ids() == ["reservoir"]
    assert system.unknown_head_node_ids() == ["demand"]
    assert system.initial_unknown_heads() == [5.0]


def test_heads_from_unknowns() -> None:
    system = build_single_pipe_system()

    heads = system.heads_from_unknowns([5.0])

    assert heads["reservoir"] == 10.0
    assert heads["demand"] == 5.0


def test_link_delta_h() -> None:
    system = build_single_pipe_system()

    heads = {
        "reservoir": 10.0,
        "demand": 5.0,
    }

    delta_h = system.link_delta_h("link_1", heads)

    assert delta_h == -5.0


def test_link_flow_rate() -> None:
    system = build_single_pipe_system()

    heads = {
        "reservoir": 10.0,
        "demand": 5.0,
    }

    q = system.link_flow_rate("link_1", heads)

    expected_q = sqrt(5.0 / 100.0)

    assert isclose(q, expected_q, rel_tol=1.0e-12, abs_tol=1.0e-12)
    assert q > 0.0


def test_all_link_flow_rates() -> None:
    system = build_single_pipe_system()

    heads = {
        "reservoir": 10.0,
        "demand": 5.0,
    }

    flows = system.all_link_flow_rates(heads)

    expected_q = sqrt(5.0 / 100.0)

    assert "link_1" in flows
    assert isclose(flows["link_1"], expected_q, rel_tol=1.0e-12, abs_tol=1.0e-12)


def test_nodal_flow_residuals_at_initial_guess() -> None:
    system = build_single_pipe_system()

    residuals = system.nodal_flow_residuals([5.0])

    expected_q = sqrt(5.0 / 100.0)
    expected_residual = -0.1 + expected_q

    assert len(residuals) == 1
    assert isclose(
        residuals[0],
        expected_residual,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_nodal_flow_residuals_at_solution() -> None:
    system = build_single_pipe_system()

    # For the demand node:
    #
    # demand = 0.1 m³/s
    # pipe law: ΔH = -100 Q²
    #
    # Required:
    #     Q = 0.1
    #     ΔH = -100 * 0.1² = -1
    #
    # Since:
    #     ΔH = H_demand - H_reservoir
    #
    # And:
    #     H_reservoir = 10
    #
    # Then:
    #     H_demand = 9
    residuals = system.nodal_flow_residuals([9.0])

    assert len(residuals) == 1
    assert isclose(residuals[0], 0.0, rel_tol=1.0e-12, abs_tol=1.0e-12)


def test_reverse_flow_case() -> None:
    system = HydraulicSystem(id="reverse_flow_system")

    reservoir = ReservoirNode(
        id="reservoir",
        parameters={
            "elevation": 0.0,
            "head": 10.0,
        },
    )

    junction = JunctionNode(
        id="junction",
        parameters={
            "elevation": 0.0,
            "initial_head": 15.0,
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
    system.add_node(junction)
    system.add_connection(pipe)

    system.connect(
        connection_id="pipe",
        from_node_id="reservoir",
        to_node_id="junction",
        link_id="link_1",
    )

    heads = {
        "reservoir": 10.0,
        "junction": 15.0,
    }

    delta_h = system.link_delta_h("link_1", heads)
    q = system.link_flow_rate("link_1", heads)

    assert delta_h == 5.0
    assert q < 0.0


def test_system_to_dict() -> None:
    system = build_single_pipe_system()

    data = system.to_dict()

    assert data["id"] == "single_pipe_system"
    assert len(data["nodes"]) == 2
    assert len(data["connections"]) == 1
    assert len(data["links"]) == 1
    assert data["links"][0]["id"] == "link_1"


def test_invalid_link_references_raise_error() -> None:
    system = HydraulicSystem(id="invalid_link_system")

    reservoir = ReservoirNode(
        id="reservoir",
        parameters={
            "elevation": 0.0,
            "head": 10.0,
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
    system.add_connection(pipe)

    try:
        system.connect(
            connection_id="pipe",
            from_node_id="reservoir",
            to_node_id="missing_node",
            link_id="invalid_link",
        )
    except ValueError as error:
        assert "unknown to_node" in str(error)
    else:
        raise AssertionError("Expected ValueError for missing to_node_id.")


def test_duplicate_node_id_raises_error() -> None:
    system = HydraulicSystem(id="duplicate_node_system")

    node_1 = JunctionNode(
        id="node",
        parameters={
            "elevation": 0.0,
            "initial_head": 10.0,
        },
    )

    node_2 = JunctionNode(
        id="node",
        parameters={
            "elevation": 0.0,
            "initial_head": 20.0,
        },
    )

    system.add_node(node_1)

    try:
        system.add_node(node_2)
    except ValueError as error:
        assert "already exists" in str(error)
    else:
        raise AssertionError("Expected ValueError for duplicated node id.")

def test_system_from_dict_round_trip() -> None:
    from hn3ttk.system import system_from_dict, system_to_dict

    system = build_single_pipe_system()

    data = system_to_dict(system)
    rebuilt = system_from_dict(data)

    assert rebuilt.id == system.id
    assert set(rebuilt.nodes.keys()) == set(system.nodes.keys())
    assert set(rebuilt.connections.keys()) == set(system.connections.keys())
    assert set(rebuilt.links.keys()) == set(system.links.keys())

    original_residuals = system.nodal_flow_residuals([5.0])
    rebuilt_residuals = rebuilt.nodal_flow_residuals([5.0])

    assert original_residuals == rebuilt_residuals

    original_state = system.evaluate_state([5.0])
    rebuilt_state = rebuilt.evaluate_state([5.0])

    assert original_state["residuals"]["max_abs"] == rebuilt_state["residuals"]["max_abs"]
    assert original_state["links"]["link_1"]["flow_rate"] == rebuilt_state["links"]["link_1"]["flow_rate"]

if __name__ == "__main__":
    test_link_creation()
    test_link_reversed()
    test_link_to_dict_and_from_dict()
    test_system_add_objects()
    test_fixed_and_unknown_node_ids()
    test_heads_from_unknowns()
    test_link_delta_h()
    test_link_flow_rate()
    test_all_link_flow_rates()
    test_nodal_flow_residuals_at_initial_guess()
    test_nodal_flow_residuals_at_solution()
    test_reverse_flow_case()
    test_system_to_dict()
    test_invalid_link_references_raise_error()
    test_duplicate_node_id_raises_error()
    test_system_from_dict_round_trip()
    
    print("All basic system tests passed.")
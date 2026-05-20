from __future__ import annotations

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, JunctionNode, ReservoirNode
from hn3ttk.system import HydraulicSystem


def _add_pipe_link(
    system: HydraulicSystem,
    *,
    connection_id: str,
    from_node_id: str,
    to_node_id: str,
    link_id: str,
    k: float,
    n: float = 2.0,
) -> None:
    """Create a PipeFixedPowerLaw connection and attach it to the system."""
    system.add_connection(
        PipeFixedPowerLaw(
            id=connection_id,
            parameters={
                "k": float(k),
                "n": float(n),
            },
        )
    )
    system.connect(
        connection_id=connection_id,
        from_node_id=from_node_id,
        to_node_id=to_node_id,
        link_id=link_id,
    )


def build_single_pipe_system() -> HydraulicSystem:
    """Build the canonical reservoir -> pipe -> demand validation case."""
    system = HydraulicSystem(id="single_pipe_system")

    system.add_node(
        ReservoirNode(
            id="reservoir",
            parameters={
                "elevation": 0.0,
                "head": 10.0,
            },
        )
    )
    system.add_node(
        DemandNode(
            id="demand",
            parameters={
                "elevation": 0.0,
                "initial_head": 5.0,
                "demand": 0.1,
            },
        )
    )

    _add_pipe_link(
        system,
        connection_id="pipe",
        from_node_id="reservoir",
        to_node_id="demand",
        link_id="link_1",
        k=100.0,
        n=2.0,
    )

    return system


def build_parallel_pipes_system() -> HydraulicSystem:
    """Build a small system with two parallel pipes feeding one junction."""
    system = HydraulicSystem(id="parallel_pipes_system")

    system.add_node(
        ReservoirNode(
            id="reservoir_high",
            parameters={
                "elevation": 0.0,
                "head": 20.0,
            },
        )
    )
    system.add_node(
        ReservoirNode(
            id="reservoir_low",
            parameters={
                "elevation": 0.0,
                "head": 10.0,
            },
        )
    )
    system.add_node(
        JunctionNode(
            id="junction",
            parameters={
                "elevation": 0.0,
                "initial_head": 15.0,
                "external_flow": 0.0,
            },
        )
    )

    _add_pipe_link(
        system,
        connection_id="pipe_1",
        from_node_id="reservoir_high",
        to_node_id="junction",
        link_id="link_high_junction_1",
        k=100.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_2",
        from_node_id="reservoir_high",
        to_node_id="junction",
        link_id="link_high_junction_2",
        k=400.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_3",
        from_node_id="junction",
        to_node_id="reservoir_low",
        link_id="link_junction_low",
        k=100.0,
    )

    return system


def build_three_reservoirs_system() -> HydraulicSystem:
    """Build a central junction connected to three fixed-head reservoirs."""
    system = HydraulicSystem(id="three_reservoirs_system")

    system.add_node(
        ReservoirNode(
            id="reservoir_high_1",
            parameters={
                "elevation": 0.0,
                "head": 30.0,
            },
        )
    )
    system.add_node(
        ReservoirNode(
            id="reservoir_high_2",
            parameters={
                "elevation": 0.0,
                "head": 20.0,
            },
        )
    )
    system.add_node(
        ReservoirNode(
            id="reservoir_low",
            parameters={
                "elevation": 0.0,
                "head": 10.0,
            },
        )
    )
    system.add_node(
        JunctionNode(
            id="central_junction",
            parameters={
                "elevation": 0.0,
                "initial_head": 15.0,
                "external_flow": 0.0,
            },
        )
    )

    _add_pipe_link(
        system,
        connection_id="pipe_high_1",
        from_node_id="reservoir_high_1",
        to_node_id="central_junction",
        link_id="link_high_1_junction",
        k=100.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_high_2",
        from_node_id="reservoir_high_2",
        to_node_id="central_junction",
        link_id="link_high_2_junction",
        k=200.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_low",
        from_node_id="central_junction",
        to_node_id="reservoir_low",
        link_id="link_junction_low",
        k=150.0,
    )

    return system


def build_hardy_cross_loop_system() -> HydraulicSystem:
    """
    Build a looped network inspired by classical Hardy-Cross examples.

    Topology:
        source -> demand_1
        demand_1 -> demand_2
        demand_2 -> demand_3
        demand_3 -> reservoir_low
        demand_1 -> demand_3

    The branch demand_1 -> demand_2 -> demand_3 and the shortcut
    demand_1 -> demand_3 provide two alternative paths and therefore a small
    looped benchmark in the graph-theoretic sense.
    """
    system = HydraulicSystem(id="hardy_cross_loop_system")

    system.add_node(
        ReservoirNode(
            id="source",
            parameters={
                "elevation": 0.0,
                "head": 50.0,
            },
        )
    )
    system.add_node(
        ReservoirNode(
            id="reservoir_low",
            parameters={
                "elevation": 0.0,
                "head": 35.0,
            },
        )
    )
    system.add_node(
        DemandNode(
            id="demand_1",
            parameters={
                "elevation": 0.0,
                "initial_head": 46.0,
                "demand": 0.03,
            },
        )
    )
    system.add_node(
        DemandNode(
            id="demand_2",
            parameters={
                "elevation": 0.0,
                "initial_head": 44.0,
                "demand": 0.02,
            },
        )
    )
    system.add_node(
        DemandNode(
            id="demand_3",
            parameters={
                "elevation": 0.0,
                "initial_head": 42.0,
                "demand": 0.04,
            },
        )
    )

    _add_pipe_link(
        system,
        connection_id="pipe_source_d1",
        from_node_id="source",
        to_node_id="demand_1",
        link_id="link_source_d1",
        k=80.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_d1_d2",
        from_node_id="demand_1",
        to_node_id="demand_2",
        link_id="link_d1_d2",
        k=140.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_d2_d3",
        from_node_id="demand_2",
        to_node_id="demand_3",
        link_id="link_d2_d3",
        k=120.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_d3_low",
        from_node_id="demand_3",
        to_node_id="reservoir_low",
        link_id="link_d3_low",
        k=90.0,
    )
    _add_pipe_link(
        system,
        connection_id="pipe_d1_d3",
        from_node_id="demand_1",
        to_node_id="demand_3",
        link_id="link_d1_d3",
        k=160.0,
    )

    return system


def build_medium_generic_network_system() -> HydraulicSystem:
    r"""
    Build a medium-size generic hydraulic network.

    ASCII sketch:

        reservoir_source
              | \
              |  \
             j1   j2
             |\   |\
             | \  | \
             |  \ |  \
             j3---+---j5
              \       |
               \      |
                j4----+
                  \   |
                   \  |
                     j6 ---- reservoir_low

    Link orientation is only a reference convention. Negative flow means the
    actual direction is opposite to the stored link orientation.
    """
    system = HydraulicSystem(id="medium_generic_network_system")

    system.add_node(
        ReservoirNode(
            id="reservoir_source",
            parameters={
                "elevation": 0.0,
                "head": 60.0,
            },
        )
    )
    system.add_node(
        ReservoirNode(
            id="reservoir_low",
            parameters={
                "elevation": 0.0,
                "head": 40.0,
            },
        )
    )

    demand_data = [
        ("junction_1", 55.0, 0.04),
        ("junction_2", 54.0, 0.03),
        ("junction_3", 52.0, 0.05),
        ("junction_4", 50.0, 0.04),
        ("junction_5", 48.0, 0.03),
        ("junction_6", 46.0, 0.02),
    ]

    for node_id, initial_head, demand in demand_data:
        system.add_node(
            DemandNode(
                id=node_id,
                parameters={
                    "elevation": 0.0,
                    "initial_head": initial_head,
                    "demand": demand,
                },
            )
        )

    pipe_data = [
        ("pipe_source_j1", "reservoir_source", "junction_1", "link_source_j1", 80.0),
        ("pipe_source_j2", "reservoir_source", "junction_2", "link_source_j2", 120.0),
        ("pipe_j1_j3", "junction_1", "junction_3", "link_j1_j3", 100.0),
        ("pipe_j2_j3", "junction_2", "junction_3", "link_j2_j3", 150.0),
        ("pipe_j3_j4", "junction_3", "junction_4", "link_j3_j4", 90.0),
        ("pipe_j4_j5", "junction_4", "junction_5", "link_j4_j5", 110.0),
        ("pipe_j5_j6", "junction_5", "junction_6", "link_j5_j6", 130.0),
        ("pipe_j6_low", "junction_6", "reservoir_low", "link_j6_low", 100.0),
        ("pipe_j2_j5", "junction_2", "junction_5", "link_j2_j5", 180.0),
        ("pipe_j1_j4", "junction_1", "junction_4", "link_j1_j4", 200.0),
        ("pipe_j3_j6", "junction_3", "junction_6", "link_j3_j6", 220.0),
    ]

    for connection_id, from_node_id, to_node_id, link_id, k in pipe_data:
        _add_pipe_link(
            system,
            connection_id=connection_id,
            from_node_id=from_node_id,
            to_node_id=to_node_id,
            link_id=link_id,
            k=k,
        )

    return system

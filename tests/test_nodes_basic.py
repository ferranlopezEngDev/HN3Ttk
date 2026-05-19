from __future__ import annotations

from hn3ttk.nodes import (
    ConfigurableNode,
    DemandNode,
    FixedHeadNode,
    InjectionNode,
    JunctionNode,
    ReservoirNode,
    available_node_types,
    node_from_dict,
    node_to_dict,
)


def test_configurable_fixed_head_node() -> None:
    node = ConfigurableNode(
        id="node_config_fixed",
        parameters={
            "elevation": 10.0,
            "fixed_head": True,
            "head": 30.0,
            "scale_head_with_alpha": True,
        },
    )

    assert node.is_fixed_head()
    assert not node.is_unknown_head()
    assert node.elevation() == 10.0
    assert node.fixed_head(alpha=0.0) == 10.0
    assert node.fixed_head(alpha=1.0) == 30.0
    assert node.initial_head() == 30.0
    assert node.external_flow() == 0.0
    assert node.pressure_head(head=30.0) == 20.0


def test_configurable_unknown_head_node() -> None:
    node = ConfigurableNode(
        id="node_config_unknown",
        parameters={
            "elevation": 5.0,
            "fixed_head": False,
            "initial_head": 20.0,
            "external_flow": -0.002,
            "scale_external_flow_with_alpha": True,
        },
    )

    assert not node.is_fixed_head()
    assert node.is_unknown_head()
    assert node.elevation() == 5.0
    assert node.initial_head() == 20.0
    assert node.external_flow(alpha=0.0) == 0.0
    assert node.external_flow(alpha=1.0) == -0.002
    assert node.pressure_head() == 15.0


def test_junction_node() -> None:
    node = JunctionNode(
        id="junction_1",
        parameters={
            "elevation": 5.0,
            "initial_head": 15.0,
        },
    )

    assert not node.is_fixed_head()
    assert node.is_unknown_head()
    assert node.elevation() == 5.0
    assert node.initial_head() == 15.0
    assert node.external_flow() == 0.0


def test_demand_node() -> None:
    node = DemandNode(
        id="demand_1",
        parameters={
            "elevation": 5.0,
            "initial_head": 20.0,
            "demand": 0.002,
        },
    )

    assert not node.is_fixed_head()
    assert node.is_unknown_head()
    assert node.elevation() == 5.0
    assert node.initial_head() == 20.0
    assert node.external_flow(alpha=0.0) == 0.0
    assert node.external_flow(alpha=1.0) == -0.002
    assert node.pressure_head() == 15.0


def test_injection_node() -> None:
    node = InjectionNode(
        id="injection_1",
        parameters={
            "elevation": 5.0,
            "initial_head": 20.0,
            "injection": 0.002,
        },
    )

    assert not node.is_fixed_head()
    assert node.is_unknown_head()
    assert node.elevation() == 5.0
    assert node.initial_head() == 20.0
    assert node.external_flow(alpha=0.0) == 0.0
    assert node.external_flow(alpha=1.0) == 0.002
    assert node.pressure_head() == 15.0


def test_fixed_head_node() -> None:
    node = FixedHeadNode(
        id="fixed_1",
        parameters={
            "elevation": 10.0,
            "head": 30.0,
        },
    )

    assert node.is_fixed_head()
    assert not node.is_unknown_head()
    assert node.elevation() == 10.0
    assert node.fixed_head() == 30.0
    assert node.initial_head() == 30.0
    assert node.external_flow() == 0.0
    assert node.pressure_head() == 20.0


def test_reservoir_node() -> None:
    node = ReservoirNode(
        id="reservoir_1",
        parameters={
            "elevation": 10.0,
            "head": 30.0,
        },
        metadata={
            "name": "Reservoir A",
        },
    )

    assert node.is_fixed_head()
    assert node.elevation() == 10.0
    assert node.fixed_head() == 30.0
    assert node.initial_head() == 30.0
    assert node.external_flow() == 0.0
    assert node.metadata["name"] == "Reservoir A"


def test_node_factory() -> None:
    data = {
        "id": "reservoir_from_dict",
        "type": "reservoir_node",
        "parameters": {
            "elevation": 10.0,
            "head": 30.0,
        },
        "metadata": {
            "name": "Reservoir from dictionary",
        },
    }

    node = node_from_dict(data)

    assert isinstance(node, ReservoirNode)
    assert node.id == "reservoir_from_dict"
    assert node.fixed_head() == 30.0
    assert node.elevation() == 10.0
    assert node.metadata["name"] == "Reservoir from dictionary"

    exported = node_to_dict(node)

    assert exported["id"] == "reservoir_from_dict"
    assert exported["type"] == "reservoir_node"
    assert exported["parameters"]["head"] == 30.0
    assert exported["metadata"]["name"] == "Reservoir from dictionary"


def test_available_node_types() -> None:
    types = available_node_types()

    assert "configurable_node" in types
    assert "junction_node" in types
    assert "fixed_head_node" in types
    assert "demand_node" in types
    assert "injection_node" in types
    assert "reservoir_node" in types


if __name__ == "__main__":
    test_configurable_fixed_head_node()
    test_configurable_unknown_head_node()
    test_junction_node()
    test_demand_node()
    test_injection_node()
    test_fixed_head_node()
    test_reservoir_node()
    test_node_factory()
    test_available_node_types()

    print("All basic node tests passed.")
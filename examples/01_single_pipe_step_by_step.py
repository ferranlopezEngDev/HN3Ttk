from __future__ import annotations

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, ReservoirNode
from hn3ttk.results import (
    links_table,
    nodes_table,
    print_result_summary,
    residuals_table,
)
from hn3ttk.solvers import solve_newton_raphson
from hn3ttk.system import HydraulicSystem


def print_rows(title: str, rows: list[dict]) -> None:
    print()
    print(title)
    for row in rows:
        print(row)


def main() -> None:
    # Step 1: Create an empty hydraulic system.
    system = HydraulicSystem(id="single_pipe_step_by_step")

    # Step 2: Define the fixed-head reservoir.
    reservoir = ReservoirNode(
        id="reservoir",
        parameters={
            "elevation": 0.0,
            "head": 10.0,
        },
    )

    # Step 3: Define the demand node.
    demand = DemandNode(
        id="demand",
        parameters={
            "elevation": 0.0,
            "initial_head": 5.0,
            "demand": 0.1,
        },
    )

    # Step 4: Define the pipe model.
    pipe = PipeFixedPowerLaw(
        id="pipe",
        parameters={
            "k": 100.0,
            "n": 2.0,
        },
    )

    # Step 5: Connect the physical pipe between the two nodes.
    system.add_node(reservoir)
    system.add_node(demand)
    system.add_connection(pipe)
    system.connect(
        connection_id="pipe",
        from_node_id="reservoir",
        to_node_id="demand",
        link_id="link_1",
    )

    print("Initial unknown heads:", system.initial_unknown_heads())
    print("Initial residuals:", system.nodal_flow_residuals(system.initial_unknown_heads()))

    # Step 6: Solve the nonlinear system.
    result = solve_newton_raphson(system)

    # Step 7: Inspect the results.
    print()
    print("Expected solution for this case:")
    print("H_demand = 9.0")
    print("Q = 0.1")
    print("delta_h = -1.0")

    print()
    print_result_summary(result)
    print_rows("Nodes table", nodes_table(result))
    print_rows("Links table", links_table(result))
    print_rows("Residuals table", residuals_table(result))


if __name__ == "__main__":
    main()

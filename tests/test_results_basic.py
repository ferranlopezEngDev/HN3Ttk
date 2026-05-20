from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.nodes import DemandNode, ReservoirNode
from hn3ttk.results import (
    export_links_csv,
    export_nodes_csv,
    export_residuals_csv,
    export_result_folder,
    export_state_json,
    export_unknown_heads_csv,
    links_table,
    nodes_table,
    residuals_table,
    result_summary,
    unknown_heads_table,
)
from hn3ttk.solvers import solve_newton_raphson
from hn3ttk.system import HydraulicSystem


def build_single_pipe_system() -> HydraulicSystem:
    system = HydraulicSystem(id="single_pipe_results_test_system")

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


def solve_single_pipe_result():
    return solve_newton_raphson(build_single_pipe_system())


def test_nodes_table_from_result() -> None:
    result = solve_single_pipe_result()
    rows = nodes_table(result)

    assert len(rows) == 2
    node_ids = {row["node_id"] for row in rows}
    assert "reservoir" in node_ids
    assert "demand" in node_ids

    demand_row = next(row for row in rows if row["node_id"] == "demand")
    assert abs(demand_row["head"] - 9.0) < 1.0e-8


def test_links_table_from_result() -> None:
    result = solve_single_pipe_result()
    rows = links_table(result)

    assert len(rows) == 1
    row = rows[0]
    assert row["link_id"] == "link_1"
    assert abs(row["flow_rate"] - 0.1) < 1.0e-8
    assert abs(row["delta_h"] - (-1.0)) < 1.0e-8


def test_residuals_table_from_result() -> None:
    result = solve_single_pipe_result()
    rows = residuals_table(result)

    assert len(rows) == 1
    row = rows[0]
    assert row["node_id"] == "demand"
    assert abs(row["residual"]) < 1.0e-8


def test_unknown_heads_table_from_result() -> None:
    result = solve_single_pipe_result()
    rows = unknown_heads_table(result)

    assert len(rows) == 1
    row = rows[0]
    assert row["node_id"] == "demand"
    assert abs(row["head"] - 9.0) < 1.0e-8


def test_result_summary_from_result() -> None:
    result = solve_single_pipe_result()
    summary = result_summary(result)

    assert summary["success"] is True
    assert summary["n_nodes"] == 2
    assert summary["n_links"] == 1
    assert summary["n_unknown_nodes"] == 1
    assert summary["n_fixed_nodes"] == 1


def test_export_result_folder() -> None:
    result = solve_single_pipe_result()

    with TemporaryDirectory() as tmp_dir:
        paths = export_result_folder(result, tmp_dir, prefix="single_pipe")

        expected_names = [
            "single_pipe_result.json",
            "single_pipe_state.json",
            "single_pipe_nodes.csv",
            "single_pipe_links.csv",
            "single_pipe_residuals.csv",
            "single_pipe_unknown_heads.csv",
        ]

        for expected_name in expected_names:
            assert Path(tmp_dir, expected_name).exists()

        with paths["result_json"].open("r", encoding="utf-8") as file_obj:
            data = json.load(file_obj)

        assert "success" in data


def test_export_individual_files_from_state() -> None:
    result = solve_single_pipe_result()
    state = result.state
    assert state is not None

    with TemporaryDirectory() as tmp_dir:
        state_json = export_state_json(state, Path(tmp_dir) / "state.json")
        nodes_csv = export_nodes_csv(state, Path(tmp_dir) / "nodes.csv")
        links_csv = export_links_csv(state, Path(tmp_dir) / "links.csv")
        residuals_csv = export_residuals_csv(
            state,
            Path(tmp_dir) / "residuals.csv",
        )
        unknown_heads_csv = export_unknown_heads_csv(
            state,
            Path(tmp_dir) / "unknown_heads.csv",
        )

        assert state_json.exists()
        assert nodes_csv.exists()
        assert links_csv.exists()
        assert residuals_csv.exists()
        assert unknown_heads_csv.exists()


if __name__ == "__main__":
    test_nodes_table_from_result()
    test_links_table_from_result()
    test_residuals_table_from_result()
    test_unknown_heads_table_from_result()
    test_result_summary_from_result()
    test_export_result_folder()
    test_export_individual_files_from_state()
    print("All basic results tests passed.")

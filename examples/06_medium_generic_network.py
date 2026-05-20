from __future__ import annotations

from hn3ttk.benchmarks import build_medium_generic_network_system
from hn3ttk.results import (
    export_result_folder,
    links_table,
    nodes_table,
    print_result_summary,
    residuals_table,
)
from hn3ttk.solvers import (
    solve_alpha_continuation_damped_newton,
    solve_scipy_least_squares,
)


def print_rows(title: str, rows: list[dict]) -> None:
    print()
    print(title)
    for row in rows:
        print(row)


def main() -> None:
    # Step 1: Load a medium-size benchmark network.
    system = build_medium_generic_network_system()

    # Step 2: Solve it with a robust custom solver.
    result = solve_alpha_continuation_damped_newton(
        system,
        alpha_steps=10,
    )

    print("Custom alpha continuation + damped Newton result")
    print_result_summary(result)

    # Step 3: Inspect node heads and pressure heads.
    print_rows("Nodes table", nodes_table(result))

    # Step 4: Inspect link flow rates.
    print_rows("Links table", links_table(result))

    # Step 5: Check residuals.
    print_rows("Residuals table", residuals_table(result))

    # Step 6: Compare with a SciPy least-squares solver.
    scipy_result = solve_scipy_least_squares(
        system,
        method="trf",
    )

    print()
    print("SciPy least_squares result")
    print_result_summary(scipy_result)
    print()
    print(
        "Residual comparison:",
        {
            "custom_solver_max_abs_residual": result.max_abs_residual,
            "scipy_least_squares_max_abs_residual": scipy_result.max_abs_residual,
        },
    )

    # Step 7: Export results.
    exported_paths = export_result_folder(
        result,
        "data/results/medium_generic_network",
        prefix="medium_network",
    )

    print()
    print("Exported files:")
    for name, path in exported_paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()

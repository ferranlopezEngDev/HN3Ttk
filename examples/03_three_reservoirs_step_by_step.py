from __future__ import annotations

from hn3ttk.benchmarks import build_three_reservoirs_system
from hn3ttk.results import links_table, nodes_table, print_result_summary
from hn3ttk.solvers import solve_alpha_continuation_damped_newton


def print_rows(title: str, rows: list[dict]) -> None:
    print()
    print(title)
    for row in rows:
        print(row)


def main() -> None:
    # This system connects one unknown central junction to several reservoirs.
    # It is useful for checking multiple fixed-head boundaries in one problem.
    system = build_three_reservoirs_system()

    result = solve_alpha_continuation_damped_newton(
        system,
        alpha_steps=8,
    )

    print_result_summary(result)
    print_rows("Nodes table", nodes_table(result))
    print_rows("Links table", links_table(result))


if __name__ == "__main__":
    main()

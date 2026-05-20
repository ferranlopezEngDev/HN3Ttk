from __future__ import annotations

from hn3ttk.benchmarks import build_parallel_pipes_system
from hn3ttk.results import links_table, print_result_summary
from hn3ttk.solvers import (
    solve_damped_newton_raphson,
    solve_scipy_root,
)


def print_rows(title: str, rows: list[dict]) -> None:
    print()
    print(title)
    for row in rows:
        print(row)


def main() -> None:
    # This benchmark has two parallel pipes from a high-head reservoir to a
    # junction, and one outlet pipe from that junction to a low-head reservoir.
    # It is useful for checking how the flow splits between parallel branches.
    system = build_parallel_pipes_system()

    print("Parallel pipes benchmark")
    print("This case is useful to verify flow splitting and continuity.")

    result = solve_damped_newton_raphson(system)

    print()
    print("Custom damped Newton result")
    print_result_summary(result)
    print_rows("Link results", links_table(result))

    scipy_result = solve_scipy_root(system, method="hybr")

    print()
    print("SciPy root (hybr) result")
    print_result_summary(scipy_result)
    print_rows("Link results", links_table(scipy_result))


if __name__ == "__main__":
    main()

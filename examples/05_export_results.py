from __future__ import annotations

from hn3ttk.benchmarks import build_single_pipe_system
from hn3ttk.results import export_result_folder, print_result_summary
from hn3ttk.solvers import solve_newton_raphson


def main() -> None:
    system = build_single_pipe_system()
    result = solve_newton_raphson(system)

    print_result_summary(result)

    exported_paths = export_result_folder(
        result,
        "data/results/example_single_pipe",
        prefix="single_pipe",
    )

    print()
    print("Generated files:")
    for name, path in exported_paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()

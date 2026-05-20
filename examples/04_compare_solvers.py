from __future__ import annotations

from hn3ttk.benchmarks import build_parallel_pipes_system, compare_solvers


def main() -> None:
    system = build_parallel_pipes_system()
    rows = compare_solvers(system)

    print("Solver comparison for the parallel pipes benchmark")
    print()
    print(
        f"{'solver':<32} {'success':<8} {'iterations':<10} "
        f"{'max_abs_residual':<18} message"
    )
    print("-" * 100)

    for row in rows:
        residual_text = f"{row['max_abs_residual']:.6g}"
        print(
            f"{row['solver']:<32} "
            f"{str(row['success']):<8} "
            f"{row['iterations']:<10} "
            f"{residual_text:<18} "
            f"{row['message']}"
        )


if __name__ == "__main__":
    main()

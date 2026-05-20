# Contributing to HN3Ttk

Thanks for your interest in HN3Ttk.

This project is currently developed as an academic hydraulic-network toolkit
focused on:

- steady-state hydraulic modelling
- nonlinear solver experimentation
- reproducible benchmarks
- beginner-friendly examples and documentation

## Recommended Setup

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/ferranlopezEngDev/HN3Ttk.git
cd HN3Ttk
pip install -e .
```

Optional development tools:

```bash
pip install -r requirements-dev.txt
```

## Local Verification

Before opening a pull request, run the same checks used in the project:

```bash
python -m py_compile hn3ttk/api.py
python -m py_compile hn3ttk/results/tables.py
python -m py_compile hn3ttk/results/summary.py
python -m py_compile hn3ttk/results/export.py
python -m py_compile hn3ttk/benchmarks/simple_networks.py
python -m py_compile hn3ttk/benchmarks/validation_cases.py
python -m py_compile hn3ttk/benchmarks/solver_comparison.py
python tests/test_connections_basic.py
python tests/test_nodes_basic.py
python tests/test_system_basic.py
python tests/test_solvers_basic.py
python tests/test_scipy_solvers_basic.py
python tests/test_results_basic.py
python tests/test_benchmarks_basic.py
python tests/test_package_metadata.py
```

You can also run the examples:

```bash
python examples/01_single_pipe_step_by_step.py
python examples/02_parallel_pipes_step_by_step.py
python examples/03_three_reservoirs_step_by_step.py
python examples/04_compare_solvers.py
python examples/05_export_results.py
python examples/06_medium_generic_network.py
```

## Style Guidelines

- Prefer explicit imports in package internals.
- Keep the current sign conventions unchanged.
- Do not break the existing public API unless the change is intentional and
  documented.
- Prefer simple type hints and dataclasses, consistent with the existing code.
- Use NumPy where dense vector and matrix operations make sense.
- Use SciPy only inside the dedicated SciPy solver wrappers unless a new module
  clearly requires it.

## Documentation

If you add a user-facing feature, please update at least one of these:

- `README.md`
- `docs/`
- `examples/`
- submodule `README.md` files

## Benchmarks and Validation

When adding or changing solver behavior:

- keep current benchmark builders reproducible
- prefer internal validation cases over undocumented ad hoc examples
- do not add external benchmark data unless its provenance and license are clear

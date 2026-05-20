# HN3Ttk

HN3Ttk 0.1.0 is an academic prototype developed for a final degree
project. It supports steady hydraulic network modelling, nonlinear residual
assembly, dense Jacobian assembly, custom Newton solvers, SciPy solver
wrappers, result export, validation examples and beginner-oriented tutorials.

## Project Status

This repository is intended for learning, prototyping and comparison of
nonlinear hydraulic solvers. It is not intended yet as a certified engineering
design tool.

## Main Features

- Nodes for fixed-head and unknown-head conditions
- Connection models for hydraulic head-loss relations
- `HydraulicSystem` for topology, residual assembly and state evaluation
- Dense Jacobian assembly with NumPy
- `SolverResult` objects with state, history and metadata
- Custom Newton-based solvers
- SciPy wrappers for `root` and `least_squares`
- JSON and CSV result export
- Reproducible internal benchmarks
- Medium generic network example
- Step-by-step examples
- Beginner-oriented documentation

## Installation

Install from a local clone in editable mode:

```bash
pip install -e .
```

Or install directly from GitHub:

Repository: [ferranlopezEngDev/HN3Ttk](https://github.com/ferranlopezEngDev/HN3Ttk)

```bash
pip install git+https://github.com/ferranlopezEngDev/HN3Ttk.git
```

## Development

Install the optional development tools with:

```bash
pip install -r requirements-dev.txt
```

To verify the repository before publishing changes, run the test scripts in
`tests/` and the step-by-step examples in `examples/`.

The repository is also prepared with a GitHub Actions CI workflow that compiles
key modules and runs tests and examples on supported Python versions.

## Quickstart

For a beginner-friendly first example, see:

- `docs/quickstart.md`
- `examples/01_single_pipe_step_by_step.py`

For quick experiments, notebooks and interactive use, you can also import the
convenience API:

```python
from hn3ttk.api import *
```

## Sign Conventions

### Connections

For passive elements:

- `q > 0 -> delta_h < 0`

### System Links

- `q > 0` means flow from `from_node_id` to `to_node_id`
- `delta_h = H_to - H_from`

### Residual

```text
residual = external_flow + inflow - outflow
```

### External Flow

- positive means injection
- negative means demand or extraction

## Solvers

| Solver | Continuation | Damping | SciPy |
|---|---|---|---|
| `solve_newton_raphson` | no | no | no |
| `solve_alpha_continuation_newton` | yes | no | no |
| `solve_damped_newton_raphson` | no | yes | no |
| `solve_alpha_continuation_damped_newton` | yes | yes | no |
| `solve_scipy_root` | no | internal SciPy | yes |
| `solve_alpha_continuation_scipy_root` | yes | internal SciPy | yes |
| `solve_scipy_least_squares` | no | internal SciPy | yes |
| `solve_alpha_continuation_scipy_least_squares` | yes | internal SciPy | yes |

## Results Export

```python
from hn3ttk.results import export_result_folder

export_result_folder(result, "data/results/single_pipe")
```

## Benchmarks

HN3Ttk currently includes:

- single pipe
- parallel pipes
- three reservoirs
- looped network inspired by Hardy-Cross examples
- medium generic network

## Tutorials and Examples

For a complete beginner tutorial, see:

`docs/quickstart.md`

For runnable step-by-step examples, see:

`examples/`

Recommended order:

1. `examples/01_single_pipe_step_by_step.py`
2. `examples/02_parallel_pipes_step_by_step.py`
3. `examples/03_three_reservoirs_step_by_step.py`
4. `examples/04_compare_solvers.py`
5. `examples/05_export_results.py`
6. `examples/06_medium_generic_network.py`

## Academic Context

- Developed as part of a final degree project
- Intended for learning, prototyping and comparison of nonlinear hydraulic solvers
- Not intended yet as a certified engineering design tool

## Roadmap

- sparse Jacobian
- EPANET `.inp` importer
- pumps and valves validation
- larger WDN benchmarks
- plots and reports
- GUI, TUI or CLI layers

# API Overview

This page summarizes the main public modules of HN3Ttk.

## `hn3ttk.nodes`

Main classes:

- `ReservoirNode`
- `DemandNode`
- `JunctionNode`
- `FixedHeadNode`
- `InjectionNode`
- `ConfigurableNode`

## `hn3ttk.connections`

Main classes:

- `Connection`
- `PipeFixedPowerLaw`
- `PipeDarcy`
- interpolation and regression-based connection models

## `hn3ttk.system`

Main classes and helpers:

- `HydraulicSystem`
- `Link`

Important methods:

- `nodal_flow_residuals(...)`
- `dense_jacobian(...)`
- `finite_difference_jacobian(...)`
- `evaluate_state(...)`

## `hn3ttk.solvers`

Main result class:

- `SolverResult`

Available solvers:

- simple Newton
- damped Newton
- alpha continuation variants
- SciPy root wrappers
- SciPy least-squares wrappers

## `hn3ttk.results`

Main helpers:

- `nodes_table(...)`
- `links_table(...)`
- `residuals_table(...)`
- `unknown_heads_table(...)`
- `result_summary(...)`
- `export_result_folder(...)`

## `hn3ttk.benchmarks`

Main content:

- benchmark builders
- validation helpers
- solver comparison helpers

# API Overview

This page summarizes the main public modules of HN3Ttk.

For model parameter dictionaries and editor-friendly `TypedDict` helpers, see:

- [Parameter Reference](parameter_reference.md)

## `hn3ttk.nodes`

Main classes:

- `ReservoirNode`
- `DemandNode`
- `JunctionNode`
- `FixedHeadNode`
- `InjectionNode`
- `ConfigurableNode`

Typed parameter helpers:

- `ReservoirNodeParameters`
- `DemandNodeParameters`
- `JunctionNodeParameters`
- `FixedHeadNodeParameters`
- `InjectionNodeParameters`
- `ConfigurableNodeParameters`

## `hn3ttk.connections`

Main classes:

- `Connection`
- `PipeFixedPowerLaw`
- `PipeDarcy`
- interpolation and regression-based connection models

Typed parameter helpers:

- `PipeFixedPowerLawParameters`
- `PipeDarcyParameters`
- `PipeLocalPowerLawParameters`
- `LinearInterpolationConnectionParameters`
- `PolynomialRegressionConnectionParameters`
- `SplineInterpolationConnectionParameters`
- `CustomFactorPolynomialConnectionParameters`

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

Literal option helpers:

- `JacobianDerivativeMode`
- `ScipyRootMethod`
- `ScipyLeastSquaresMethod`

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

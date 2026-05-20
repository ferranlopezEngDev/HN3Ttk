# Benchmarks Module

The `benchmarks` module contains small reproducible hydraulic systems that can
be used for validation, regression testing, solver comparison and teaching.

The currently included cases are:

- single pipe
- parallel pipes
- three reservoirs
- looped network inspired by classical Hardy-Cross examples
- medium generic network

## What Each Case Tests

- `single_pipe`: analytical validation, sign conventions and first solver tests
- `parallel_pipes`: flow splitting and one junction with multiple incident links
- `three_reservoirs`: one unknown node connected to several fixed-head nodes
- `hardy_cross_loop`: a small looped network with alternative paths
- `medium_generic_network`: a more realistic internal benchmark for robust
  solvers, exports and tutorials

## Recommended Solvers

- `single_pipe`: simple Newton-Raphson, damped Newton or SciPy wrappers
- `parallel_pipes`: damped Newton or `scipy_root(method="hybr")`
- `three_reservoirs`: damped Newton or `scipy_root(method="hybr")`
- `hardy_cross_loop`: alpha continuation with damped Newton or
  `scipy_least_squares(method="trf")`
- `medium_generic_network`: alpha continuation with damped Newton or
  `scipy_least_squares(method="trf")`

These cases are internal and reproducible. They are useful for development and
teaching, but they do not replace validation against EPANET or another external
reference simulator.

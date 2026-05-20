# Benchmarks Guide

HN3Ttk includes several internal validation and benchmark cases.

## Single Pipe

Objective:

- validate sign conventions
- validate solver setup
- compare against an analytical result

Recommended solver:

- `solve_newton_raphson`

Expected checks:

- demand head close to 9.0
- link flow close to 0.1
- `delta_h` close to -1.0

## Parallel Pipes

Objective:

- test flow splitting
- test continuity at one unknown junction

Recommended solver:

- `solve_damped_newton_raphson`
- `solve_scipy_root(method="hybr")`

## Three Reservoirs

Objective:

- test one unknown node connected to several fixed-head reservoirs
- observe how the solver balances several branches

Recommended solver:

- `solve_damped_newton_raphson`
- `solve_scipy_root(method="hybr")`

## Looped Network Inspired by Hardy-Cross

Objective:

- test a looped topology with alternative paths
- verify continuity across several unknown nodes

Recommended solver:

- `solve_alpha_continuation_damped_newton`
- `solve_scipy_least_squares(method="trf")`

## Medium Generic Network

This network contains:

- 8 nodes
- 11 links
- 6 unknown heads
- 2 fixed-head reservoirs
- several demand nodes
- looped paths

It is useful for:

- testing solver robustness
- exporting results
- comparing custom solvers against SciPy wrappers

Recommended solver:

- `solve_alpha_continuation_damped_newton`
- `solve_scipy_least_squares(method="trf")`

Do not infer external benchmark-grade validation from this case alone. It is an
internal generic network designed for reproducible package testing and teaching.

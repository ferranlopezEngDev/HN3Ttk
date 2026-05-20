# Solvers Guide

HN3Ttk currently provides custom Newton solvers and SciPy wrappers.

## Available Solvers

- `solve_newton_raphson`
- `solve_alpha_continuation_newton`
- `solve_damped_newton_raphson`
- `solve_alpha_continuation_damped_newton`
- `solve_scipy_root`
- `solve_alpha_continuation_scipy_root`
- `solve_scipy_least_squares`
- `solve_alpha_continuation_scipy_least_squares`

## Decision Table

| Situation | Solver recommended |
|---|---|
| Case pequeño y bien condicionado | Newton simple |
| Problema sensible al punto inicial | Alpha continuation |
| Newton da pasos excesivos | Damped Newton |
| Problema difícil | Alpha continuation + damped |
| Comparación con SciPy | `scipy_root` with `hybr` |
| Sistema mal condicionado | `scipy_least_squares` with `trf` |
| Red genérica mediana | alpha continuation + damped o `scipy_least_squares(method="trf")` |

## Important Parameters

### `tolerance`

Controls when the solver considers the residual small enough.

### `residual_tolerance`

Used by the SciPy wrappers to require that the final residual is not only
accepted by SciPy, but also small enough for HN3Ttk validation.

### `max_iterations`

Maximum number of nonlinear iterations for the custom Newton solvers.

### `derivative_mode`

Controls how the system Jacobian is assembled through each connection:

- `default`
- `normal`
- `tendency`
- `inverse_head_loss`
- `finite_difference`

### `alpha_steps`

Number of continuation steps between `alpha_start` and `alpha_end`.

### Damping Parameters

The damped solver includes:

- `initial_damping_factor`
- `damping_reduction_factor`
- `min_damping_factor`
- `max_backtracking_steps`

### `use_jacobian`

For SciPy wrappers:

- `solve_scipy_root` uses the analytical Jacobian only when the selected method
  supports it directly, especially `hybr` and `lm`
- `solve_scipy_least_squares` uses the analytical Jacobian whenever
  `use_jacobian=True`

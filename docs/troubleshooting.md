# Troubleshooting

## 1. The solver does not converge

Possible cause:

- poor initial guess
- difficult looped network

What to try:

- use `solve_damped_newton_raphson`
- use `solve_alpha_continuation_damped_newton`
- compare with `solve_scipy_least_squares(method="trf")`

## 2. The Jacobian is singular

Possible cause:

- disconnected topology
- redundant or insufficient constraints
- zero-flow singular behavior near the initial point

What to try:

- inspect the network connectivity
- review fixed-head nodes
- try a more robust continuation or least-squares solver

## 3. The residual does not decrease

Possible cause:

- Newton steps are too aggressive
- the initial guess is too far from the solution

What to try:

- switch from simple Newton to damped Newton
- increase `alpha_steps`

## 4. The flow is negative

Possible cause:

- nothing is necessarily wrong

Interpretation:

- the actual flow goes opposite to the stored link orientation

## 5. Pressure head is negative

Possible cause:

- the computed hydraulic head is below elevation

What to do:

- inspect node elevations
- inspect demands and boundary heads
- verify whether negative pressure is physically acceptable in your study

## 6. The system has disconnected nodes

Possible cause:

- a node was added but not linked

What to do:

- inspect `system.links`
- verify that every unknown-head node participates in the network

## 7. Too many fixed-head nodes or no unknown nodes

Possible cause:

- the network is over-constrained or trivial

What to do:

- review which nodes should be fixed head
- ensure at least one unknown-head node exists for a nontrivial solve

## 8. The link orientation seems inverted

Possible cause:

- the chosen reference direction is opposite to the actual solved flow

What to do:

- keep the orientation if it is readable
- interpret negative flow as reverse direction

## 9. SciPy converges but `residual_tolerance` is not satisfied

Possible cause:

- SciPy accepted its own stopping criterion before the residual became small
  enough for your validation target

What to do:

- reduce tolerances
- use a stricter `residual_tolerance`
- compare with damped Newton

## 10. Alpha continuation fails at an intermediate alpha

Possible cause:

- the step in alpha is too large

What to try:

- increase `alpha_steps`
- use the damped continuation solver
- compare with `scipy_least_squares(method="trf")`

## 11. The medium network converges with SciPy but not with simple Newton

Possible cause:

- simple Newton can be too sensitive for a coupled looped network

What to do:

- use `solve_alpha_continuation_damped_newton`
- use `solve_scipy_least_squares(method="trf")`
- inspect residuals and initial heads

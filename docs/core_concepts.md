# Core Concepts

HN3Ttk separates the hydraulic problem into local objects and a global system
assembler.

## Node

A node contains local nodal information:

- elevation
- fixed-head or unknown-head behavior
- external flow

Examples:

- `ReservoirNode`
- `DemandNode`
- `JunctionNode`

External flow convention:

- positive: injection into the network
- negative: demand or extraction

## Connection

A connection contains a local hydraulic relation such as `head_loss(q)` or
`flow_rate(delta_h)`.

Important:

- a connection does not know which nodes it is attached to
- it only knows its own physical model

## Link

A link attaches one connection to two nodes and defines orientation:

```text
from_node ---- connection ---- to_node
```

Link convention:

- `q > 0` means flow from `from_node_id` to `to_node_id`
- `delta_h = H_to - H_from`

If a solved flow is negative, the actual flow direction is opposite to the
reference orientation of the link.

## HydraulicSystem

`HydraulicSystem` owns:

- nodes
- connections
- links

The system is responsible for:

- topology
- complete head reconstruction
- residual assembly
- dense Jacobian assembly
- full state evaluation

## Residual

For each unknown-head node, HN3Ttk assembles a mass-balance residual:

```text
residual = external_flow + inflow - outflow
```

At the solution:

```text
residual = 0
```

## Jacobian

The Jacobian is the derivative of the residual vector with respect to the
unknown heads:

```text
J = dR/dH
```

HN3Ttk currently assembles a dense Jacobian with NumPy.

## SolverResult

A solver returns a `SolverResult` containing:

- success flag
- message
- iterations
- solved unknown heads
- residual vector
- maximum absolute residual
- optional evaluated `state`
- history
- metadata

## State

`state` is a post-processed dictionary created by `system.evaluate_state(...)`.
It contains:

- node results
- link results
- residuals
- unknown and fixed node ids

## Alpha Continuation

Alpha continuation solves a sequence of problems:

```text
R(H, alpha) = 0
```

starting from a simpler case such as `alpha = 0` and progressing to
`alpha = 1`.

## Damping

Damping reduces the full Newton step when that step is too aggressive. In
HN3Ttk, the damped solver uses backtracking to search for a smaller step that
reduces the residual.

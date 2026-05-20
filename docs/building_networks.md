# Building Networks

This guide explains how to move from a tiny network to a medium-size example.

## A Single Pipe

The smallest complete case is:

```text
reservoir -> demand
```

You create:

1. a `HydraulicSystem`
2. nodes
3. one connection
4. one link with `system.connect(...)`

See:

- `docs/quickstart.md`
- `examples/01_single_pipe_step_by_step.py`

## Several Pipes

With more than one pipe, you keep the same pattern:

1. define nodes
2. define connections
3. connect them with links

Parallel pipes are useful to check flow splitting.

## Several Reservoirs

A network can have several fixed-head boundary nodes. This is common when you
want to test how an unknown junction balances flow against multiple sources or
boundary levels.

## Looped Networks

A looped network has alternative paths between parts of the graph. These
networks are usually more interesting numerically because the residuals and
flows depend on several interacting routes.

## Choosing Link Orientations

Link orientation is a reference convention. Choose a direction that is easy to
read and keep it consistent.

If the solved flow is negative:

- nothing is wrong
- it simply means the actual flow goes opposite to the link orientation

## Demands, Injections and Fixed Heads

- Use `DemandNode` for positive demand magnitudes stored as extraction
- Use `JunctionNode` for a generic unknown-head node with optional external flow
- Use `ReservoirNode` or `FixedHeadNode` for prescribed hydraulic head

## Medium-size Generic Networks

When moving from a tiny case to a network with several unknown nodes:

- use clear ids
- keep a readable naming convention for links and pipes
- orient links consistently
- expect some solved flows to become negative
- prefer robust solvers if the network is looped or strongly coupled
- inspect residuals after solving

See:

`examples/06_medium_generic_network.py`

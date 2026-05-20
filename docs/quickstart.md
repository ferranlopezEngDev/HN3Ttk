# Quickstart

This quickstart builds and solves the simplest HN3Ttk network:

`reservoir -> pipe -> demand`

Install the package in editable mode:

```bash
pip install -e .
```

Basic imports:

```python
from hn3ttk.nodes import ReservoirNode, DemandNode
from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.system import HydraulicSystem
from hn3ttk.solvers import solve_newton_raphson
from hn3ttk.results import (
    nodes_table,
    links_table,
    result_summary,
    export_result_folder,
)
```

Complete example:

```python
from hn3ttk.nodes import ReservoirNode, DemandNode
from hn3ttk.connections import PipeFixedPowerLaw
from hn3ttk.system import HydraulicSystem
from hn3ttk.solvers import solve_newton_raphson
from hn3ttk.results import (
    nodes_table,
    links_table,
    result_summary,
    export_result_folder,
)

system = HydraulicSystem(id="quickstart_single_pipe")

reservoir = ReservoirNode(
    id="reservoir",
    parameters={
        "elevation": 0.0,
        "head": 10.0,
    },
)

demand = DemandNode(
    id="demand",
    parameters={
        "elevation": 0.0,
        "initial_head": 5.0,
        "demand": 0.1,
    },
)

pipe = PipeFixedPowerLaw(
    id="pipe",
    parameters={
        "k": 100.0,
        "n": 2.0,
    },
)

system.add_node(reservoir)
system.add_node(demand)
system.add_connection(pipe)
system.connect(
    connection_id="pipe",
    from_node_id="reservoir",
    to_node_id="demand",
    link_id="link_1",
)

result = solve_newton_raphson(system)

print(result_summary(result))
print(nodes_table(result))
print(links_table(result))

export_result_folder(result, "data/results/quickstart_single_pipe")
```

The same example is available as a runnable script:

`examples/01_single_pipe_step_by_step.py`

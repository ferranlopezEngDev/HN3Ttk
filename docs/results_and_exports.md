# Results and Exports

## SolverResult

Every solver returns a `SolverResult` containing:

- `success`
- `message`
- `iterations`
- `unknown_heads`
- `residuals`
- `max_abs_residual`
- `state`
- `history`
- `metadata`

## State

`result.state` is created from `system.evaluate_state(...)` and contains:

- full node results
- full link results
- residuals by node
- unknown and fixed node ids

## Tables

The `hn3ttk.results` module provides flat table helpers:

- `nodes_table(result)`
- `links_table(result)`
- `residuals_table(result)`
- `unknown_heads_table(result)`

These return `list[dict]` and do not depend on pandas.

## JSON Export

- `export_state_json(...)`
- `export_result_json(...)`

## CSV Export

- `export_nodes_csv(...)`
- `export_links_csv(...)`
- `export_residuals_csv(...)`
- `export_unknown_heads_csv(...)`

## Complete Export Folder

```python
from hn3ttk.results import export_result_folder

export_result_folder(result, "data/results/single_pipe")
```

This writes:

- result JSON
- state JSON
- nodes CSV
- links CSV
- residuals CSV
- unknown-heads CSV

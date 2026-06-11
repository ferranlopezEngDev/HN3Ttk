# Plot Examples

This folder is the right place for scripts that visualize the behaviour of
connection models.

Why here:

- They are exploratory and educational scripts, not core library code.
- They fit naturally next to the existing `examples/` tutorials.
- They can evolve quickly without forcing a public plotting API inside
  `hn3ttk/`.

Recommended convention:

1. Put one focused plotting scenario per script.
2. Use numbered filenames when the scripts form a small learning sequence.
3. Save generated figures under `data/results/plots/` when running headless or
   when an explicit output path is requested.

Current script:

1. `01_plot_darcy_local_power_law_regimes.py`
2. `02_plot_tabulated_curve_resolution_methods.py`
3. `03_plot_all_connection_models.py`

Run from the repository root:

```bash
python examples/plots/01_plot_darcy_local_power_law_regimes.py
```

Save directly to a file:

```bash
python examples/plots/01_plot_darcy_local_power_law_regimes.py \
  --output data/results/plots/darcy_local_power_law_regimes.png
```

```bash
python examples/plots/02_plot_tabulated_curve_resolution_methods.py
```

```bash
python examples/plots/02_plot_tabulated_curve_resolution_methods.py \
  --output data/results/plots/tabulated_curve_resolution_methods.png
```

```bash
python examples/plots/03_plot_all_connection_models.py
```

```bash
python examples/plots/03_plot_all_connection_models.py \
  --output data/results/plots/all_connection_models_plot_methods.png
```

If these plots eventually become a reusable product feature instead of examples,
then the next logical home would be a new package such as `hn3ttk/visualization/`.

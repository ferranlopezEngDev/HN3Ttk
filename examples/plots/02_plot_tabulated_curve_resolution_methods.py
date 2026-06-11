from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

if os.name != "nt" and not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from hn3ttk.connections import (
    LinearInterpolationConnection,
    PolynomialRegressionConnection,
    SplineInterpolationConnection,
    SplineSecantExtrapolationConnection,
    SplineTangentExtrapolationConnection,
)


DEFAULT_FLOW_RATES = [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]
DEFAULT_HEAD_LOSSES = [42.0, 39.3, 34.8, 28.4, 19.7, 8.2]
DEFAULT_POLYNOMIAL_DEGREE = 3
DEFAULT_OUTPUT = Path("data/results/plots/tabulated_curve_resolution_methods.png")

MODEL_STYLES = {
    "Linear interpolation": {"color": "#0b7189"},
    "Polynomial regression (deg=3)": {"color": "#ef6f6c"},
    "Spline interpolation (pchip)": {"color": "#355070"},
    "Spline interpolation (cubic_spline)": {"color": "#e9c46a"},
    "Spline tangent extrapolation (pchip)": {"color": "#6a4c93"},
    "Spline secant extrapolation (pchip)": {"color": "#2a9d8f"},
}


def build_models() -> dict[str, object]:
    base_parameters = {
        "flow_rates": list(DEFAULT_FLOW_RATES),
        "head_losses": list(DEFAULT_HEAD_LOSSES),
        # Needed so the symmetric tendency can evaluate H(-Q) for one-sided
        # pump tabulations that only provide positive-flow samples.
        "extrapolate": True,
    }
    return {
        "Linear interpolation": LinearInterpolationConnection(
            parameters=dict(base_parameters)
        ),
        "Polynomial regression (deg=3)": PolynomialRegressionConnection(
            parameters={
                **base_parameters,
                "degree": DEFAULT_POLYNOMIAL_DEGREE,
            }
        ),
        "Spline interpolation (pchip)": SplineInterpolationConnection(
            parameters={
                **base_parameters,
                "method": "pchip",
            }
        ),
        "Spline interpolation (cubic_spline)": SplineInterpolationConnection(
            parameters={
                **base_parameters,
                "method": "cubic_spline",
            }
        ),
        "Spline tangent extrapolation (pchip)": SplineTangentExtrapolationConnection(
            parameters={
                **base_parameters,
                "method": "pchip",
            }
        ),
        "Spline secant extrapolation (pchip)": SplineSecantExtrapolationConnection(
            parameters={
                **base_parameters,
                "method": "pchip",
            }
        ),
    }


def add_combined_legend(primary_axis: plt.Axes, secondary_axis: plt.Axes) -> None:
    primary_handles, primary_labels = primary_axis.get_legend_handles_labels()
    secondary_handles, secondary_labels = secondary_axis.get_legend_handles_labels()
    primary_axis.legend(
        primary_handles + secondary_handles,
        primary_labels + secondary_labels,
        loc="lower center",
        ncols=4,
        fontsize=8,
        frameon=True,
    )


def build_figure() -> plt.Figure:
    flow_values = np.array(DEFAULT_FLOW_RATES, dtype=float)
    head_values = np.array(DEFAULT_HEAD_LOSSES, dtype=float)
    models = build_models()
    flow_abs_max = float(np.max(np.abs(flow_values)))
    dense_flow_values = np.linspace(-flow_abs_max, flow_abs_max, 1200)
    model_curves: dict[str, dict[str, np.ndarray]] = {}
    head_min = float("inf")
    head_max = float("-inf")
    secondary_min = float("inf")
    secondary_max = float("-inf")

    for model_name, connection in models.items():
        plot_data = connection.head_loss_plot_data(
            q_start=-flow_abs_max,
            q_end=flow_abs_max,
            n=len(dense_flow_values),
        )
        direct_curve = np.array(plot_data["head_losses"])
        derivative_curve = np.array(plot_data["derivatives"])
        tendency_curve = np.array(plot_data["tendencies"])

        model_curves[model_name] = {
            "head": direct_curve,
            "derivative": derivative_curve,
            "tendency": tendency_curve,
        }
        head_min = min(head_min, float(np.min(direct_curve)))
        head_max = max(head_max, float(np.max(direct_curve)))
        secondary_min = min(
            secondary_min,
            float(np.min(derivative_curve)),
            float(np.min(tendency_curve)),
        )
        secondary_max = max(
            secondary_max,
            float(np.max(derivative_curve)),
            float(np.max(tendency_curve)),
        )

    figure, axes = plt.subplots(3, 2, figsize=(15, 14), constrained_layout=True)
    figure.suptitle(
        "Tabulated pump curve: one twin-axis panel per interpolation/regression option",
        fontsize=14,
    )
    head_padding = 0.07 * (head_max - head_min)
    secondary_padding = 0.07 * (secondary_max - secondary_min)

    for axis, model_name in zip(axes.flat, models):
        style = MODEL_STYLES[model_name]
        secondary_axis = axis.twinx()

        axis.scatter(
            flow_values,
            head_values,
            s=38,
            color="#1f1f1f",
            label="tabulated points",
            zorder=4,
        )
        axis.plot(
            dense_flow_values,
            model_curves[model_name]["head"],
            color=style["color"],
            linewidth=2.6,
            label="H(Q)",
        )
        secondary_axis.plot(
            dense_flow_values,
            model_curves[model_name]["derivative"],
            color=style["color"],
            linestyle="--",
            linewidth=2.2,
            label="dH/dQ",
        )
        secondary_axis.plot(
            dense_flow_values,
            model_curves[model_name]["tendency"],
            color=style["color"],
            linestyle=":",
            linewidth=2.4,
            label="tendency",
        )

        axis.axhline(0.0, color="#666666", linestyle="--", linewidth=1.0)
        axis.axvline(0.0, color="#666666", linestyle="--", linewidth=1.0)
        secondary_axis.axhline(0.0, color="#999999", linestyle=":", linewidth=0.9)

        axis.set_title(model_name)
        axis.set_xlabel("Flow rate Q [m3/s]")
        axis.set_ylabel("Head H [m]")
        secondary_axis.set_ylabel("dH/dQ and tendency")
        axis.grid(True, alpha=0.25)
        axis.set_xlim(-flow_abs_max, flow_abs_max)
        axis.set_ylim(head_min - head_padding, head_max + head_padding)
        secondary_axis.set_ylim(
            secondary_min - secondary_padding,
            secondary_max + secondary_padding,
        )
        add_combined_legend(axis, secondary_axis)

    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot one twin-axis panel per tabulated-curve resolution option, "
            "showing H(Q), dH/dQ and tendency."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output PNG path.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Force displaying the figure even if an output path is provided.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    figure = build_figure()

    can_show = matplotlib.get_backend().lower() != "agg"
    output_path = args.output

    if output_path is None and not can_show:
        output_path = DEFAULT_OUTPUT

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=160, bbox_inches="tight")
        print(f"Plot saved to {output_path}")

    if args.show or (output_path is None and can_show):
        plt.show()
    else:
        plt.close(figure)


if __name__ == "__main__":
    main()

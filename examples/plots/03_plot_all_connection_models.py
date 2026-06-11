from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

if os.name != "nt" and not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

from hn3ttk.connections import (
    Connection,
    CustomFactorPolynomialConnection,
    LinearInterpolationConnection,
    PipeDarcy,
    PipeFixedPowerLaw,
    PipeLocalPowerLaw,
    PolynomialRegressionConnection,
    SplineInterpolationConnection,
    SplineSecantExtrapolationConnection,
    SplineTangentExtrapolationConnection,
)


DEFAULT_OUTPUT = Path("data/results/plots/all_connection_models_plot_methods.png")
PIPE_PARAMETERS = {
    "length": 100.0,
    "diameter": 0.05,
    "roughness": 1.5e-4,
}
TABULATED_PARAMETERS = {
    "flow_rates": [-0.02, -0.01, 0.0, 0.01, 0.02],
    "head_losses": [3.0, 1.0, 0.0, -1.0, -3.0],
    "extrapolate": True,
}

MODEL_COLORS = [
    "#0b7189",
    "#ef6f6c",
    "#355070",
    "#e9c46a",
    "#6a4c93",
    "#2a9d8f",
    "#bc6c25",
    "#3a7d44",
    "#7f5539",
]


def build_models() -> list[tuple[str, Connection, float]]:
    return [
        (
            "PipeDarcy",
            PipeDarcy(parameters=dict(PIPE_PARAMETERS)),
            4.8e-4,
        ),
        (
            "PipeLocalPowerLaw",
            PipeLocalPowerLaw(parameters=dict(PIPE_PARAMETERS)),
            4.8e-4,
        ),
        (
            "PipeFixedPowerLaw",
            PipeFixedPowerLaw(
                parameters={
                    "k": 120.0,
                    "n": 2.0,
                }
            ),
            0.12,
        ),
        (
            "CustomFactorPolynomial",
            CustomFactorPolynomialConnection(
                parameters={
                    "coefficients": [10.0, 120.0],
                    "exponents": [1.0, 2.0],
                }
            ),
            0.12,
        ),
        (
            "LinearInterpolation",
            LinearInterpolationConnection(parameters=dict(TABULATED_PARAMETERS)),
            0.03,
        ),
        (
            "PolynomialRegression",
            PolynomialRegressionConnection(
                parameters={
                    **TABULATED_PARAMETERS,
                    "degree": 3,
                }
            ),
            0.03,
        ),
        (
            "SplineInterpolation",
            SplineInterpolationConnection(
                parameters={
                    **TABULATED_PARAMETERS,
                    "method": "pchip",
                }
            ),
            0.03,
        ),
        (
            "SplineTangentExtrapolation",
            SplineTangentExtrapolationConnection(
                parameters={
                    **TABULATED_PARAMETERS,
                    "method": "pchip",
                }
            ),
            0.03,
        ),
        (
            "SplineSecantExtrapolation",
            SplineSecantExtrapolationConnection(
                parameters={
                    **TABULATED_PARAMETERS,
                    "method": "pchip",
                }
            ),
            0.03,
        ),
    ]


def add_panel(
    ax: plt.Axes,
    *,
    x_values: list[float],
    curve_values: list[float],
    derivative_values: list[float],
    tendency_values: list[float],
    title: str,
    x_label: str,
    y_label: str,
    secondary_y_label: str,
    color: str,
    curve_label: str,
    derivative_label: str,
) -> None:
    secondary_axis = ax.twinx()

    ax.plot(
        x_values,
        curve_values,
        color=color,
        linewidth=2.4,
        label=curve_label,
    )
    secondary_axis.plot(
        x_values,
        derivative_values,
        color=color,
        linestyle="--",
        linewidth=2.0,
        label=derivative_label,
    )
    secondary_axis.plot(
        x_values,
        tendency_values,
        color=color,
        linestyle=":",
        linewidth=2.2,
        label="tendency",
    )

    ax.axhline(0.0, color="#666666", linestyle="--", linewidth=1.0)
    ax.axvline(0.0, color="#666666", linestyle="--", linewidth=1.0)
    secondary_axis.axhline(0.0, color="#999999", linestyle=":", linewidth=0.9)

    ax.set_title(title, fontsize=11)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    secondary_axis.set_ylabel(secondary_y_label)
    ax.grid(True, alpha=0.25)

    primary_handles, primary_labels = ax.get_legend_handles_labels()
    secondary_handles, secondary_labels = secondary_axis.get_legend_handles_labels()
    ax.legend(
        primary_handles + secondary_handles,
        primary_labels + secondary_labels,
        loc="lower center",
        ncols=3,
        fontsize=7,
        frameon=True,
    )


def build_figure() -> plt.Figure:
    models = build_models()
    n_rows = len(models)
    figure, axes = plt.subplots(
        n_rows,
        2,
        figsize=(16, 3.2 * n_rows),
        constrained_layout=True,
    )
    figure.suptitle(
        "All connection models using the generic plot-data helpers",
        fontsize=15,
    )

    if n_rows == 1:
        axes = [axes]

    n_points = 600

    for row_axes, (index, (name, connection, q_abs_max)) in zip(
        axes,
        enumerate(models),
    ):
        color = MODEL_COLORS[index % len(MODEL_COLORS)]
        direct_data = connection.head_loss_plot_data(
            q_start=-q_abs_max,
            q_end=q_abs_max,
            n=n_points,
        )
        head_abs_max = max(abs(value) for value in direct_data["head_losses"])
        inverse_data = connection.flow_rate_plot_data(
            delta_h_start=-head_abs_max,
            delta_h_end=head_abs_max,
            n=n_points,
        )

        add_panel(
            row_axes[0],
            x_values=direct_data["flow_rates"],
            curve_values=direct_data["head_losses"],
            derivative_values=direct_data["derivatives"],
            tendency_values=direct_data["tendencies"],
            title=f"{name}: H(Q)",
            x_label="Flow rate Q [m3/s]",
            y_label="Head H [m]",
            secondary_y_label="dH/dQ and tendency",
            color=color,
            curve_label="H(Q)",
            derivative_label="dH/dQ",
        )
        add_panel(
            row_axes[1],
            x_values=inverse_data["head_losses"],
            curve_values=inverse_data["flow_rates"],
            derivative_values=inverse_data["derivatives"],
            tendency_values=inverse_data["tendencies"],
            title=f"{name}: Q(H)",
            x_label="Head H [m]",
            y_label="Flow rate Q [m3/s]",
            secondary_y_label="dQ/dH and tendency",
            color=color,
            curve_label="Q(H)",
            derivative_label="dQ/dH",
        )

    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot all implemented connection models using the generic "
            "head_loss_plot_data and flow_rate_plot_data helpers."
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

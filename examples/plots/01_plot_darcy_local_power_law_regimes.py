from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib

if os.name != "nt" and not os.environ.get("DISPLAY"):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from hn3ttk.connections import PipeDarcy, PipeLocalPowerLaw


DEFAULT_PARAMETERS = {
    "length": 100.0,
    "diameter": 0.05,
    "roughness": 1.5e-4,
}
DEFAULT_OUTPUT = Path("data/results/plots/darcy_local_power_law_regimes.png")


def build_models() -> tuple[PipeDarcy, PipeLocalPowerLaw]:
    darcy = PipeDarcy(parameters=dict(DEFAULT_PARAMETERS))
    local = PipeLocalPowerLaw(parameters=dict(DEFAULT_PARAMETERS))
    return darcy, local


def shade_direct_regimes(
    ax: plt.Axes,
    laminar_flow_limit: float,
    turbulent_flow_limit: float,
    flow_max: float,
) -> None:
    ax.axvspan(-flow_max, -turbulent_flow_limit, color="#fddbc7", alpha=0.35)
    ax.axvspan(-turbulent_flow_limit, -laminar_flow_limit, color="#fee8c8", alpha=0.45)
    ax.axvspan(-laminar_flow_limit, laminar_flow_limit, color="#d9f0d3", alpha=0.45)
    ax.axvspan(laminar_flow_limit, turbulent_flow_limit, color="#fee8c8", alpha=0.45)
    ax.axvspan(turbulent_flow_limit, flow_max, color="#fddbc7", alpha=0.35)

    for x_value in (
        -turbulent_flow_limit,
        -laminar_flow_limit,
        laminar_flow_limit,
        turbulent_flow_limit,
    ):
        ax.axvline(x_value, color="#4d4d4d", linestyle="--", linewidth=1.0)


def shade_inverse_regimes(
    ax: plt.Axes,
    laminar_head_limit: float,
    turbulent_head_limit: float,
    head_max: float,
) -> None:
    ax.axvspan(-head_max, -turbulent_head_limit, color="#fddbc7", alpha=0.35)
    ax.axvspan(-turbulent_head_limit, -laminar_head_limit, color="#fee8c8", alpha=0.45)
    ax.axvspan(-laminar_head_limit, laminar_head_limit, color="#d9f0d3", alpha=0.45)
    ax.axvspan(laminar_head_limit, turbulent_head_limit, color="#fee8c8", alpha=0.45)
    ax.axvspan(turbulent_head_limit, head_max, color="#fddbc7", alpha=0.35)

    for x_value in (
        -turbulent_head_limit,
        -laminar_head_limit,
        laminar_head_limit,
        turbulent_head_limit,
        ):
        ax.axvline(x_value, color="#4d4d4d", linestyle="--", linewidth=1.0)


def build_flow_regime_spans(
    laminar_flow_limit: float,
    turbulent_flow_limit: float,
    flow_max: float,
) -> list[tuple[float, float, str]]:
    return [
        (-flow_max, -turbulent_flow_limit, "Turbulent"),
        (-turbulent_flow_limit, -laminar_flow_limit, "Transition"),
        (-laminar_flow_limit, laminar_flow_limit, "Laminar"),
        (laminar_flow_limit, turbulent_flow_limit, "Transition"),
        (turbulent_flow_limit, flow_max, "Turbulent"),
    ]


def build_head_regime_spans(
    laminar_head_limit: float,
    turbulent_head_limit: float,
    head_max: float,
) -> list[tuple[float, float, str]]:
    return [
        (-head_max, -turbulent_head_limit, "Turbulent"),
        (-turbulent_head_limit, -laminar_head_limit, "Transition"),
        (-laminar_head_limit, laminar_head_limit, "Laminar"),
        (laminar_head_limit, turbulent_head_limit, "Transition"),
        (turbulent_head_limit, head_max, "Turbulent"),
    ]


def add_regime_labels(
    ax: plt.Axes,
    spans: list[tuple[float, float, str]],
    min_width_fraction: float = 0.12,
) -> None:
    xmin, xmax = ax.get_xlim()
    visible_width = xmax - xmin
    ymin, ymax = ax.get_ylim()
    y_text = ymin + 0.93 * (ymax - ymin)
    for start, end, label in spans:
        if (end - start) / visible_width < min_width_fraction:
            continue
        ax.text(
            0.5 * (start + end),
            y_text,
            label,
            ha="center",
            va="center",
            fontsize=9,
        )


def add_combined_legend(primary_axis: plt.Axes, secondary_axis: plt.Axes) -> None:
    primary_handles, primary_labels = primary_axis.get_legend_handles_labels()
    secondary_handles, secondary_labels = secondary_axis.get_legend_handles_labels()
    primary_axis.legend(
        primary_handles + secondary_handles,
        primary_labels + secondary_labels,
        loc="lower center",
        ncols=3,
        fontsize=8,
        frameon=True,
    )


def plot_panel(
    ax: plt.Axes,
    *,
    x_values: np.ndarray,
    curve_values: np.ndarray,
    derivative_values: np.ndarray,
    tendency_values: np.ndarray,
    title: str,
    x_label: str,
    y_label: str,
    secondary_y_label: str,
    curve_label: str,
    derivative_label: str,
    color: str,
    shade_function,
    shade_args: tuple[float, float, float],
    regime_spans: list[tuple[float, float, str]],
    regime_label_min_width: float,
) -> None:
    secondary_axis = ax.twinx()

    shade_function(ax, *shade_args)

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
        alpha=0.8,
        label="tendency",
    )

    ax.axhline(0.0, color="#4d4d4d", linestyle="--", linewidth=1.0)
    ax.axvline(0.0, color="#4d4d4d", linestyle="--", linewidth=1.0)
    secondary_axis.axhline(0.0, color="#9a9a9a", linestyle=":", linewidth=0.9)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    secondary_axis.set_ylabel(secondary_y_label)
    ax.grid(True, alpha=0.25)
    ax.set_xlim(float(x_values[0]), float(x_values[-1]))

    add_regime_labels(ax, regime_spans, min_width_fraction=regime_label_min_width)
    add_combined_legend(ax, secondary_axis)


def build_figure() -> plt.Figure:
    darcy, local = build_models()
    flow_max = 4.8e-4
    flow_values = np.linspace(-flow_max, flow_max, 1200)

    darcy_head_loss_values = np.array(
        [darcy.head_loss(flow_rate) for flow_rate in flow_values]
    )
    darcy_head_loss_derivative_values = np.array(
        [darcy.head_loss_derivative(flow_rate) for flow_rate in flow_values]
    )
    darcy_head_loss_tendency_values = np.array(
        [darcy.head_loss_tendency(flow_rate) for flow_rate in flow_values]
    )
    local_head_loss_values = np.array(
        [local.head_loss(flow_rate) for flow_rate in flow_values]
    )
    local_head_loss_derivative_values = np.array(
        [local.head_loss_derivative(flow_rate) for flow_rate in flow_values]
    )
    local_head_loss_tendency_values = np.array(
        [local.head_loss_tendency(flow_rate) for flow_rate in flow_values]
    )

    head_abs_max = max(
        float(np.max(np.abs(darcy_head_loss_values))),
        float(np.max(np.abs(local_head_loss_values))),
    )
    head_values = np.linspace(-head_abs_max, head_abs_max, 1200)

    darcy_flow_rate_values = np.array(
        [darcy.flow_rate(delta_h) for delta_h in head_values]
    )
    darcy_flow_rate_derivative_values = np.array(
        [darcy.flow_rate_derivative(delta_h) for delta_h in head_values]
    )
    darcy_flow_rate_tendency_values = np.array(
        [darcy.flow_rate_tendency(delta_h) for delta_h in head_values]
    )
    local_flow_rate_values = np.array(
        [local.flow_rate(delta_h) for delta_h in head_values]
    )
    local_flow_rate_derivative_values = np.array(
        [local.flow_rate_derivative(delta_h) for delta_h in head_values]
    )
    local_flow_rate_tendency_values = np.array(
        [local.flow_rate_tendency(delta_h) for delta_h in head_values]
    )

    laminar_flow_limit = darcy._flow_rate_from_reynolds(
        float(darcy.parameters["laminar_reynolds"])
    )
    turbulent_flow_limit = darcy._flow_rate_from_reynolds(
        float(darcy.parameters["turbulent_reynolds"])
    )
    darcy_laminar_head_limit = abs(darcy.head_loss(laminar_flow_limit))
    darcy_turbulent_head_limit = abs(darcy.head_loss(turbulent_flow_limit))
    local_laminar_head_limit = abs(local.head_loss(laminar_flow_limit))
    local_turbulent_head_limit = abs(local.head_loss(turbulent_flow_limit))
    flow_regime_spans = build_flow_regime_spans(
        laminar_flow_limit,
        turbulent_flow_limit,
        flow_max,
    )
    darcy_head_regime_spans = build_head_regime_spans(
        darcy_laminar_head_limit,
        darcy_turbulent_head_limit,
        head_abs_max,
    )
    local_head_regime_spans = build_head_regime_spans(
        local_laminar_head_limit,
        local_turbulent_head_limit,
        head_abs_max,
    )

    figure, axes = plt.subplots(2, 2, figsize=(15, 10), constrained_layout=True)
    figure.suptitle(
        "PipeDarcy and PipeLocalPowerLaw: curves, derivatives and tendencies",
        fontsize=14,
    )

    plot_panel(
        axes[0, 0],
        x_values=flow_values,
        curve_values=darcy_head_loss_values,
        derivative_values=darcy_head_loss_derivative_values,
        tendency_values=darcy_head_loss_tendency_values,
        title="PipeDarcy: H(Q), derivative and tendency",
        x_label="Flow rate Q [m3/s]",
        y_label="Head loss ΔH [m]",
        secondary_y_label="d(ΔH)/dQ and tendency",
        curve_label="ΔH(Q)",
        derivative_label="d(ΔH)/dQ",
        color="#0b7189",
        shade_function=shade_direct_regimes,
        shade_args=(laminar_flow_limit, turbulent_flow_limit, flow_max),
        regime_spans=flow_regime_spans,
        regime_label_min_width=0.09,
    )
    plot_panel(
        axes[0, 1],
        x_values=head_values,
        curve_values=darcy_flow_rate_values,
        derivative_values=darcy_flow_rate_derivative_values,
        tendency_values=darcy_flow_rate_tendency_values,
        title="PipeDarcy: Q(ΔH), derivative and tendency",
        x_label="Head loss ΔH [m]",
        y_label="Flow rate Q [m3/s]",
        secondary_y_label="dQ/d(ΔH) and tendency",
        curve_label="Q(ΔH)",
        derivative_label="dQ/d(ΔH)",
        color="#0b7189",
        shade_function=shade_inverse_regimes,
        shade_args=(darcy_laminar_head_limit, darcy_turbulent_head_limit, head_abs_max),
        regime_spans=darcy_head_regime_spans,
        regime_label_min_width=0.12,
    )
    plot_panel(
        axes[1, 0],
        x_values=flow_values,
        curve_values=local_head_loss_values,
        derivative_values=local_head_loss_derivative_values,
        tendency_values=local_head_loss_tendency_values,
        title="PipeLocalPowerLaw: H(Q), derivative and tendency",
        x_label="Flow rate Q [m3/s]",
        y_label="Head loss ΔH [m]",
        secondary_y_label="d(ΔH)/dQ and tendency",
        curve_label="ΔH(Q)",
        derivative_label="d(ΔH)/dQ",
        color="#ef6f6c",
        shade_function=shade_direct_regimes,
        shade_args=(laminar_flow_limit, turbulent_flow_limit, flow_max),
        regime_spans=flow_regime_spans,
        regime_label_min_width=0.09,
    )
    plot_panel(
        axes[1, 1],
        x_values=head_values,
        curve_values=local_flow_rate_values,
        derivative_values=local_flow_rate_derivative_values,
        tendency_values=local_flow_rate_tendency_values,
        title="PipeLocalPowerLaw: Q(ΔH), derivative and tendency",
        x_label="Head loss ΔH [m]",
        y_label="Flow rate Q [m3/s]",
        secondary_y_label="dQ/d(ΔH) and tendency",
        curve_label="Q(ΔH)",
        derivative_label="dQ/d(ΔH)",
        color="#ef6f6c",
        shade_function=shade_inverse_regimes,
        shade_args=(local_laminar_head_limit, local_turbulent_head_limit, head_abs_max),
        regime_spans=local_head_regime_spans,
        regime_label_min_width=0.12,
    )

    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot the direct curves ΔH(Q) and the inverse curves Q(ΔH) for "
            "PipeDarcy and PipeLocalPowerLaw."
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

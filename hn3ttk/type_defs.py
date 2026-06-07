"""
Type definitions for editor-friendly HN3Ttk usage.

These aliases and TypedDict objects are intended to improve autocompletion in
editors such as VS Code while keeping the runtime API unchanged.
"""

from __future__ import annotations

from typing import Literal, TypedDict

JacobianDerivativeMode = Literal[
    "default",
    "normal",
    "tendency",
    "inverse_head_loss",
    "finite_difference",
]

ScipyRootMethod = Literal[
    "hybr",
    "lm",
    "broyden1",
    "broyden2",
    "anderson",
    "linearmixing",
    "diagbroyden",
    "excitingmixing",
    "krylov",
    "df-sane",
]

ScipyLeastSquaresMethod = Literal[
    "trf",
    "dogbox",
    "lm",
]

SplineInterpolationMethod = Literal[
    "pchip",
    "cubic_spline",
]


class ConnectionDerivativeParameters(TypedDict, total=False):
    """Common optional parameters accepted by all connection models."""

    jacobian_derivative: JacobianDerivativeMode
    jacobian_derivative_step: float
    jacobian_derivative_absolute_step: float


class ConfigurableNodeParameters(TypedDict, total=False):
    """Parameters accepted by ConfigurableNode."""

    elevation: float
    fixed_head: bool
    head: float
    initial_head: float
    external_flow: float
    scale_head_with_alpha: bool
    scale_external_flow_with_alpha: bool


class JunctionNodeParameters(TypedDict, total=False):
    """Parameters accepted by JunctionNode."""

    elevation: float
    initial_head: float
    external_flow: float
    scale_external_flow_with_alpha: bool
    fixed_head: bool


class FixedHeadNodeParameters(TypedDict, total=False):
    """Parameters accepted by FixedHeadNode."""

    elevation: float
    head: float
    scale_head_with_alpha: bool
    fixed_head: bool
    external_flow: float
    scale_external_flow_with_alpha: bool


class ReservoirNodeParameters(FixedHeadNodeParameters, total=False):
    """Parameters accepted by ReservoirNode."""


class DemandNodeParameters(TypedDict, total=False):
    """Parameters accepted by DemandNode."""

    elevation: float
    initial_head: float
    demand: float
    scale_demand_with_alpha: bool


class InjectionNodeParameters(TypedDict, total=False):
    """Parameters accepted by InjectionNode."""

    elevation: float
    initial_head: float
    injection: float
    scale_injection_with_alpha: bool


class PipeFixedPowerLawParameters(ConnectionDerivativeParameters, total=False):
    """Parameters accepted by PipeFixedPowerLaw."""

    k: float
    n: float
    head_tolerance: float


class PipeDarcyParameters(ConnectionDerivativeParameters, total=False):
    """Parameters accepted by PipeDarcy."""

    length: float
    diameter: float
    roughness: float
    kinematic_viscosity: float
    gravity: float
    laminar_reynolds: float
    turbulent_reynolds: float
    head_tolerance: float
    inverse_relative_tolerance: float
    inverse_max_iterations: int
    derivative_relative_step: float
    derivative_absolute_step: float


class PipeLocalPowerLawParameters(ConnectionDerivativeParameters, total=False):
    """Parameters accepted by PipeLocalPowerLaw."""

    length: float
    diameter: float
    roughness: float
    kinematic_viscosity: float
    gravity: float
    laminar_reynolds: float
    turbulent_reynolds: float
    relative_band: float
    minimum_flow_rate: float
    head_tolerance: float
    inverse_relative_tolerance: float
    inverse_max_iterations: int
    derivative_relative_step: float
    derivative_absolute_step: float


class LinearInterpolationConnectionParameters(
    ConnectionDerivativeParameters,
    total=False,
):
    """Parameters accepted by LinearInterpolationConnection."""

    flow_rates: list[float]
    head_losses: list[float]
    extrapolate: bool


class PolynomialRegressionConnectionParameters(
    ConnectionDerivativeParameters,
    total=False,
):
    """Parameters accepted by PolynomialRegressionConnection."""

    flow_rates: list[float]
    head_losses: list[float]
    degree: int
    extrapolate: bool
    inverse_scan_points: int
    inverse_max_iterations: int
    head_tolerance: float
    flow_tolerance: float


class SplineInterpolationConnectionParameters(
    ConnectionDerivativeParameters,
    total=False,
):
    """Parameters accepted by SplineInterpolationConnection."""

    flow_rates: list[float]
    head_losses: list[float]
    method: SplineInterpolationMethod
    extrapolate: bool


class CustomFactorPolynomialConnectionParameters(
    ConnectionDerivativeParameters,
    total=False,
):
    """Parameters accepted by CustomFactorPolynomialConnection."""

    coefficients: list[float]
    exponents: list[float]
    head_tolerance: float
    inverse_relative_tolerance: float
    inverse_max_iterations: int
    minimum_flow_rate: float

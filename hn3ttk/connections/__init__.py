from hn3ttk.connections.base import Connection
from hn3ttk.connections.custom_factor_polynomial import (
    CustomFactorPolynomialConnection,
)
from hn3ttk.connections.linear_interpolation import LinearInterpolationConnection
from hn3ttk.connections.pipe_darcy import PipeDarcy
from hn3ttk.connections.pipe_fixed_power_law import PipeFixedPowerLaw
from hn3ttk.connections.pipe_local_power_law import PipeLocalPowerLaw
from hn3ttk.connections.polynomial_regression import PolynomialRegressionConnection
from hn3ttk.connections.spline_interpolation import SplineInterpolationConnection

__all__ = [
    "Connection",
    "CustomFactorPolynomialConnection",
    "LinearInterpolationConnection",
    "PipeDarcy",
    "PipeFixedPowerLaw",
    "PipeLocalPowerLaw",
    "PolynomialRegressionConnection",
    "SplineInterpolationConnection",
]
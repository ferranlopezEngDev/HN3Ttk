from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import copysign, isfinite
from typing import Any, ClassVar
from uuid import uuid4


@dataclass
class Connection(ABC):
    """
    Base class for hydraulic connection models.

    A Connection represents only the local physical behaviour of an
    hydraulic element. It does not know which nodes it connects.
    """

    id: str = field(default_factory=lambda: f"conn_{uuid4().hex}")
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    type: ClassVar[str] = "connection"
    jacobian_derivative_modes: ClassVar[tuple[str, ...]] = (
        "default",
        "normal",
        "tendency",
        "inverse_head_loss",
        "finite_difference",
    )

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def head_loss(self, q: float) -> float:
        """Return head loss for a given flow rate."""
        raise NotImplementedError

    @abstractmethod
    def flow_rate(self, delta_h: float) -> float:
        """Return flow rate for a given head difference."""
        raise NotImplementedError

    @abstractmethod
    def head_loss_derivative(self, q: float) -> float:
        """Return d(delta_h)/dQ."""
        raise NotImplementedError

    @abstractmethod
    def flow_rate_derivative(self, delta_h: float) -> float:
        """Return dQ/d(delta_h)."""
        raise NotImplementedError

    def head_loss_tendency(self, q: float) -> float:
        """
        Return the symmetric secant tendency of the head-loss curve.

        tendency = [head_loss(q) - head_loss(-q)] / (2q)
        """
        if q == 0:
            return self.head_loss_derivative(0.0)

        return (self.head_loss(q) - self.head_loss(-q)) / (2.0 * q)

    def flow_rate_tendency(self, delta_h: float) -> float:
        """
        Return the symmetric secant tendency of the flow-rate curve.

        tendency = [flow_rate(delta_h) - flow_rate(-delta_h)] / (2 delta_h)
        """
        if delta_h == 0:
            return self.flow_rate_derivative(0.0)

        return (self.flow_rate(delta_h) - self.flow_rate(-delta_h)) / (
            2.0 * delta_h
        )

    @staticmethod
    def _validate_jacobian_derivative_mode(mode: str) -> str:
        """Validate and normalize a jacobian derivative mode."""
        if not isinstance(mode, str):
            raise ValueError(
                "Jacobian derivative mode must be a string. "
                "Allowed values are: "
                f"{Connection.jacobian_derivative_modes}."
            )

        mode = mode.strip()

        if mode not in Connection.jacobian_derivative_modes:
            raise ValueError(
                f"Invalid jacobian derivative mode '{mode}'. "
                "Allowed values are: "
                f"{Connection.jacobian_derivative_modes}."
            )

        return mode

    def _resolve_jacobian_derivative_mode(self, method: str) -> str:
        """Resolve a requested derivative method to a concrete strategy."""
        method = self._validate_jacobian_derivative_mode(method)

        if method != "default":
            return method

        configured_mode = self._validate_jacobian_derivative_mode(
            self.parameters.get("jacobian_derivative", "normal")
        )

        if configured_mode == "default":
            return "normal"

        return configured_mode

    def get_jacobian_derivative_mode(self) -> str:
        """Return the configured default jacobian derivative mode."""
        return self._validate_jacobian_derivative_mode(
            self.parameters.get("jacobian_derivative", "normal")
        )

    def set_jacobian_derivative_mode(self, mode: str) -> None:
        """Set the configured default jacobian derivative mode."""
        self.parameters["jacobian_derivative"] = (
            self._validate_jacobian_derivative_mode(mode)
        )

    def _finite_difference_flow_rate_derivative(self, delta_h: float) -> float:
        """Return dQ/d(delta_h) using a central finite difference."""
        delta_h = float(delta_h)

        relative_step = float(self.parameters["jacobian_derivative_step"])
        absolute_step = float(
            self.parameters["jacobian_derivative_absolute_step"]
        )

        step = max(
            absolute_step,
            relative_step * max(abs(delta_h), 1.0),
        )

        q_plus = self.flow_rate(delta_h + step)
        q_minus = self.flow_rate(delta_h - step)

        return (q_plus - q_minus) / (2.0 * step)

    def jacobian_derivative(
        self,
        delta_h: float,
        method: str = "default",
    ) -> float:
        """Return dQ/d(delta_h) using the requested jacobian strategy."""
        delta_h = float(delta_h)
        resolved_method = self._resolve_jacobian_derivative_mode(method)

        if resolved_method == "normal":
            return self.flow_rate_derivative(delta_h)

        if resolved_method == "tendency":
            return self.flow_rate_tendency(delta_h)

        if resolved_method == "inverse_head_loss":
            q = self.flow_rate(delta_h)
            d_head_d_flow = self.head_loss_derivative(q)

            if d_head_d_flow == 0.0:
                tendency = self.head_loss_tendency(q)

                if tendency != 0.0:
                    return copysign(float("inf"), tendency)

                return float("inf")

            return 1.0 / d_head_d_flow

        return self._finite_difference_flow_rate_derivative(delta_h)

    def validate(self) -> None:
        """Validate common connection data."""
        if not isinstance(self.id, str):
            raise TypeError("Connection id must be a string.")

        if not self.id:
            raise ValueError("Connection id cannot be empty.")

        if not isinstance(self.parameters, dict):
            raise TypeError("Connection parameters must be a dictionary.")

        if not isinstance(self.metadata, dict):
            raise TypeError("Connection metadata must be a dictionary.")

        self.parameters.setdefault("jacobian_derivative", "normal")
        self.parameters.setdefault("jacobian_derivative_step", 1.0e-6)
        self.parameters.setdefault(
            "jacobian_derivative_absolute_step",
            1.0e-10,
        )

        self.parameters["jacobian_derivative"] = (
            self._validate_jacobian_derivative_mode(
                self.parameters["jacobian_derivative"]
            )
        )

        for name in (
            "jacobian_derivative_step",
            "jacobian_derivative_absolute_step",
        ):
            value = self.parameters[name]

            if not isinstance(value, (int, float)):
                raise TypeError(f"Parameter '{name}' must be numeric.")

            if not isfinite(float(value)):
                raise ValueError(f"Parameter '{name}' must be finite.")

            value = float(value)

            if value <= 0.0:
                raise ValueError(f"Parameter '{name}' must be positive.")

            self.parameters[name] = value

    def to_dict(self) -> dict[str, Any]:
        """Convert the connection to a serializable dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "parameters": self.parameters,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Connection":
        """Build a connection object from a dictionary."""
        return cls(
            id=data["id"],
            parameters=data.get("parameters", {}),
            metadata=data.get("metadata", {}),
        )

    def model_info(self) -> dict[str, Any]:
        """Return basic information about the connection model."""
        return {
            "type": self.type,
            "description": "Base hydraulic connection model.",
            "parameters": [
                "jacobian_derivative",
                "jacobian_derivative_step",
                "jacobian_derivative_absolute_step",
            ],
        }

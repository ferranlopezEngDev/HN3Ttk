from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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
            "parameters": [],
        }
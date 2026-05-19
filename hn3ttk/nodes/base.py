from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import isfinite
from typing import Any, ClassVar
from uuid import uuid4


@dataclass
class Node(ABC):
    """
    Base class for hydraulic network nodes.

    A Node represents local nodal data only. It does not know which connections
    are attached to it. The system assembler is responsible for topology,
    incidence relations and residual assembly.

    External flow sign convention:
        external_flow > 0  -> injection into the network
        external_flow < 0  -> demand/extraction from the network
    """

    id: str = field(default_factory=lambda: f"node_{uuid4().hex}")
    parameters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    type: ClassVar[str] = "node"

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def is_fixed_head(self) -> bool:
        """Return True if the node has a prescribed hydraulic head."""
        raise NotImplementedError

    def is_unknown_head(self) -> bool:
        """Return True if the node hydraulic head is an unknown."""
        return not self.is_fixed_head()

    @abstractmethod
    def fixed_head(self, alpha: float = 1.0) -> float:
        """Return prescribed hydraulic head H."""
        raise NotImplementedError

    @abstractmethod
    def initial_head(self) -> float:
        """Return initial hydraulic-head guess H."""
        raise NotImplementedError

    @abstractmethod
    def external_flow(self, alpha: float = 1.0) -> float:
        """
        Return signed external nodal flow.

        Positive means injection into the network.
        Negative means demand/extraction from the network.
        """
        raise NotImplementedError

    def elevation(self) -> float:
        """Return node geometric elevation z."""
        return float(self.parameters.get("elevation", 0.0))

    def pressure_head(
        self,
        head: float | None = None,
        alpha: float = 1.0,
    ) -> float:
        """
        Return pressure head H - z.

        If head is not provided:
            - fixed-head nodes use fixed_head(alpha)
            - unknown-head nodes use initial_head()
        """
        if head is None:
            if self.is_fixed_head():
                head = self.fixed_head(alpha)
            else:
                head = self.initial_head()

        return float(head) - self.elevation()

    def validate(self) -> None:
        """Validate common node data."""
        if not isinstance(self.id, str):
            raise TypeError("Node id must be a string.")

        if not self.id:
            raise ValueError("Node id cannot be empty.")

        if not isinstance(self.parameters, dict):
            raise TypeError("Node parameters must be a dictionary.")

        if not isinstance(self.metadata, dict):
            raise TypeError("Node metadata must be a dictionary.")

    def to_dict(self) -> dict[str, Any]:
        """Convert the node to a serializable dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "parameters": self.parameters,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        """Build a node object from a dictionary."""
        return cls(
            id=data["id"],
            parameters=data.get("parameters", {}),
            metadata=data.get("metadata", {}),
        )

    def model_info(self) -> dict[str, Any]:
        """Return basic information about the node model."""
        return {
            "type": self.type,
            "description": "Base hydraulic node model.",
            "parameters": [],
        }

    @staticmethod
    def _validate_continuation_factor(alpha: float) -> float:
        """Validate and return continuation factor alpha."""
        alpha = float(alpha)

        if not isfinite(alpha):
            raise ValueError("Continuation factor 'alpha' must be finite.")

        if alpha < 0.0 or alpha > 1.0:
            raise ValueError("Continuation factor 'alpha' must be between 0 and 1.")

        return alpha

    def _validate_finite_float(self, name: str) -> None:
        """Validate that a parameter exists and is a finite numeric value."""
        if name not in self.parameters:
            raise ValueError(f"Missing parameter '{name}'.")

        value = self.parameters[name]

        if not isinstance(value, (int, float)):
            raise TypeError(f"Parameter '{name}' must be numeric.")

        if not isfinite(float(value)):
            raise ValueError(f"Parameter '{name}' must be finite.")

        self.parameters[name] = float(value)

    def _validate_bool(self, name: str) -> None:
        """Validate that a parameter exists and is boolean."""
        if name not in self.parameters:
            raise ValueError(f"Missing parameter '{name}'.")

        if not isinstance(self.parameters[name], bool):
            raise TypeError(f"Parameter '{name}' must be a boolean.")
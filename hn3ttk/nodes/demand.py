from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from hn3ttk.nodes.base import Node
from hn3ttk.type_defs import DemandNodeParameters


@dataclass
class DemandNode(Node):
    """
    Unknown-head node with prescribed demand.

    Demand is stored as a positive magnitude and returned as negative external
    flow, because it extracts water from the network.
    """

    type: ClassVar[str] = "demand_node"
    parameters: DemandNodeParameters = field(
        default_factory=lambda: cast(DemandNodeParameters, {})
    )

    def is_fixed_head(self) -> bool:
        """Demand nodes have unknown hydraulic head."""
        return False

    def fixed_head(self, alpha: float = 1.0) -> float:
        """Demand nodes do not have fixed hydraulic head."""
        self._validate_continuation_factor(alpha)
        raise ValueError("DemandNode does not have a fixed hydraulic head.")

    def initial_head(self) -> float:
        """Return initial hydraulic-head guess H."""
        return float(self.parameters["initial_head"])

    def external_flow(self, alpha: float = 1.0) -> float:
        """Return demand as negative external flow."""
        alpha = self._validate_continuation_factor(alpha)

        demand = float(self.parameters["demand"])

        if self._scale_demand_with_alpha():
            return -alpha * demand

        return -demand

    def validate(self) -> None:
        """Validate demand node parameters."""
        super().validate()

        self.parameters.setdefault("elevation", 0.0)
        self._validate_finite_float("elevation")

        self.parameters.setdefault("initial_head", self.elevation())
        self._validate_finite_float("initial_head")

        if "demand" not in self.parameters:
            raise ValueError("DemandNode requires parameter 'demand'.")

        self._validate_finite_float("demand")

        if self.parameters["demand"] < 0.0:
            raise ValueError("DemandNode parameter 'demand' cannot be negative.")

        self.parameters.setdefault("scale_demand_with_alpha", True)
        self._validate_bool("scale_demand_with_alpha")

    def model_info(self) -> dict[str, Any]:
        """Return descriptive information about this node model."""
        return {
            "type": self.type,
            "description": "Unknown-head node with prescribed demand.",
            "parameters": [
                "elevation",
                "initial_head",
                "demand",
                "scale_demand_with_alpha",
            ],
        }

    def _scale_demand_with_alpha(self) -> bool:
        return bool(self.parameters["scale_demand_with_alpha"])

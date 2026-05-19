from __future__ import annotations

from typing import Any, ClassVar

from hn3ttk.nodes.base import Node


class ConfigurableNode(Node):
    """
    Fully configurable hydraulic node.

    Parameters
    ----------
    elevation:
        Geometric elevation z [m].

    fixed_head:
        If True, the node hydraulic head is prescribed.
        If False, the node hydraulic head is an unknown.

    head:
        Prescribed hydraulic head H [m] when fixed_head is True.

    initial_head:
        Initial guess for hydraulic head H [m] when fixed_head is False.

    external_flow:
        Signed external nodal flow [m³/s].
        Positive means injection.
        Negative means demand/extraction.

    scale_head_with_alpha:
        If True:
            fixed_head(alpha) = elevation + alpha * (head - elevation)

    scale_external_flow_with_alpha:
        If True:
            external_flow(alpha) = alpha * external_flow
    """

    type: ClassVar[str] = "configurable_node"

    def is_fixed_head(self) -> bool:
        """Return True if the node has a prescribed hydraulic head."""
        return bool(self.parameters["fixed_head"])

    def fixed_head(self, alpha: float = 1.0) -> float:
        """Return prescribed hydraulic head H."""
        if not self.is_fixed_head():
            raise ValueError("Node does not have a fixed hydraulic head.")

        alpha = self._validate_continuation_factor(alpha)

        head = self._head()

        if self._scale_head_with_alpha():
            return self.elevation() + alpha * (head - self.elevation())

        return head

    def initial_head(self) -> float:
        """Return initial hydraulic-head guess H."""
        if self.is_fixed_head():
            return self.fixed_head(alpha=1.0)

        return self._initial_head()

    def external_flow(self, alpha: float = 1.0) -> float:
        """Return signed external nodal flow."""
        alpha = self._validate_continuation_factor(alpha)

        value = self._external_flow()

        if self._scale_external_flow_with_alpha():
            return alpha * value

        return value

    def validate(self) -> None:
        """Validate configurable node parameters."""
        super().validate()

        self.parameters.setdefault("elevation", 0.0)
        self._validate_finite_float("elevation")

        self.parameters.setdefault("fixed_head", False)
        self._validate_bool("fixed_head")

        self.parameters.setdefault("head", self.elevation())
        self._validate_finite_float("head")

        self.parameters.setdefault("initial_head", self.elevation())
        self._validate_finite_float("initial_head")

        self.parameters.setdefault("external_flow", 0.0)
        self._validate_finite_float("external_flow")

        self.parameters.setdefault("scale_head_with_alpha", False)
        self._validate_bool("scale_head_with_alpha")

        self.parameters.setdefault("scale_external_flow_with_alpha", True)
        self._validate_bool("scale_external_flow_with_alpha")

    def model_info(self) -> dict[str, Any]:
        """Return descriptive information about this node model."""
        return {
            "type": self.type,
            "description": "Fully configurable hydraulic node.",
            "parameters": [
                "elevation",
                "fixed_head",
                "head",
                "initial_head",
                "external_flow",
                "scale_head_with_alpha",
                "scale_external_flow_with_alpha",
            ],
        }

    def _head(self) -> float:
        return float(self.parameters["head"])

    def _initial_head(self) -> float:
        return float(self.parameters["initial_head"])

    def _external_flow(self) -> float:
        return float(self.parameters["external_flow"])

    def _scale_head_with_alpha(self) -> bool:
        return bool(self.parameters["scale_head_with_alpha"])

    def _scale_external_flow_with_alpha(self) -> bool:
        return bool(self.parameters["scale_external_flow_with_alpha"])
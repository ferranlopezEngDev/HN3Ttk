from __future__ import annotations

from typing import Any, ClassVar

from hn3ttk.nodes.configurable import ConfigurableNode


class FixedHeadNode(ConfigurableNode):
    """
    Fixed hydraulic-head boundary node.

    This node prescribes hydraulic head H. It does not impose an external flow.
    The exchanged flow is determined by the network solution.
    """

    type: ClassVar[str] = "fixed_head_node"

    def external_flow(self, alpha: float = 1.0) -> float:
        """Fixed-head boundaries do not impose an external nodal flow."""
        self._validate_continuation_factor(alpha)
        return 0.0

    def validate(self) -> None:
        """Validate fixed-head node parameters."""
        if "fixed_head" in self.parameters and self.parameters["fixed_head"] is not True:
            raise ValueError("FixedHeadNode must have fixed_head=True.")

        if "head" not in self.parameters:
            raise ValueError("FixedHeadNode requires parameter 'head'.")

        if "external_flow" in self.parameters and float(self.parameters["external_flow"]) != 0.0:
            raise ValueError("FixedHeadNode cannot impose an external_flow.")

        self.parameters["fixed_head"] = True
        self.parameters["external_flow"] = 0.0
        self.parameters["scale_external_flow_with_alpha"] = False

        super().validate()

    def model_info(self) -> dict[str, Any]:
        """Return descriptive information about this node model."""
        return {
            "type": self.type,
            "description": "Prescribed hydraulic-head boundary node.",
            "parameters": [
                "elevation",
                "head",
                "scale_head_with_alpha",
            ],
        }
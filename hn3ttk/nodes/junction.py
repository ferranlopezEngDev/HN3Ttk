from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from hn3ttk.nodes.configurable import ConfigurableNode
from hn3ttk.type_defs import JunctionNodeParameters


@dataclass
class JunctionNode(ConfigurableNode):
    """
    Junction node with unknown hydraulic head.

    It may optionally include an external flow term.
    """

    type: ClassVar[str] = "junction_node"
    parameters: JunctionNodeParameters = field(
        default_factory=lambda: cast(JunctionNodeParameters, {})
    )

    def validate(self) -> None:
        """Validate junction node parameters."""
        if "fixed_head" in self.parameters and self.parameters["fixed_head"] is not False:
            raise ValueError("JunctionNode cannot have fixed_head=True.")

        self.parameters["fixed_head"] = False
        self.parameters.setdefault("external_flow", 0.0)

        super().validate()

    def model_info(self) -> dict[str, Any]:
        """Return descriptive information about this node model."""
        return {
            "type": self.type,
            "description": "Unknown-head junction node.",
            "parameters": [
                "elevation",
                "initial_head",
                "external_flow",
                "scale_external_flow_with_alpha",
            ],
        }

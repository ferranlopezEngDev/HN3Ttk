from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, cast

from hn3ttk.nodes.fixed_head import FixedHeadNode
from hn3ttk.type_defs import ReservoirNodeParameters


@dataclass
class ReservoirNode(FixedHeadNode):
    """
    Reservoir node.

    This is a semantic fixed-head node. The prescribed hydraulic head represents
    the reservoir water surface head.
    """

    type: ClassVar[str] = "reservoir_node"
    parameters: ReservoirNodeParameters = field(
        default_factory=lambda: cast(ReservoirNodeParameters, {})
    )

    def model_info(self) -> dict[str, Any]:
        """Return descriptive information about this node model."""
        return {
            "type": self.type,
            "description": "Reservoir represented as a prescribed-head boundary.",
            "parameters": [
                "elevation",
                "head",
                "scale_head_with_alpha",
            ],
        }

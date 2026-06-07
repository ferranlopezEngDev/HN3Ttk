from __future__ import annotations

from typing import Any, ClassVar

from hn3ttk.nodes.fixed_head import FixedHeadNode


class ReservoirNode(FixedHeadNode):
    """
    Reservoir node.

    This is a semantic fixed-head node. The prescribed hydraulic head represents
    the reservoir water surface head.
    """

    type: ClassVar[str] = "reservoir_node"

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
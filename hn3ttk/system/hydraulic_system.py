from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hn3ttk.connections import Connection
from hn3ttk.nodes import Node
from hn3ttk.system.link import Link


@dataclass
class HydraulicSystem:
    """
    Hydraulic network system.

    The system owns:
        - nodes
        - connections
        - links between nodes and connections

    Connections do not know which nodes they connect.
    Nodes do not know which connections are attached to them.

    The system is responsible for topology and residual assembly.

    Link convention:
        q > 0 means flow from link.from_node_id to link.to_node_id

    Head convention:
        delta_h = H_to - H_from
    """

    id: str = "hydraulic_system"
    nodes: dict[str, Node] = field(default_factory=dict)
    connections: dict[str, Connection] = field(default_factory=dict)
    links: dict[str, Link] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.validate()

    # ------------------------------------------------------------------
    # Basic validation
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """Validate system containers."""
        if not isinstance(self.id, str):
            raise TypeError("System id must be a string.")

        if not self.id:
            raise ValueError("System id cannot be empty.")

        if not isinstance(self.nodes, dict):
            raise TypeError("System nodes must be a dictionary.")

        if not isinstance(self.connections, dict):
            raise TypeError("System connections must be a dictionary.")

        if not isinstance(self.links, dict):
            raise TypeError("System links must be a dictionary.")

        if not isinstance(self.metadata, dict):
            raise TypeError("System metadata must be a dictionary.")

        for node_id, node in self.nodes.items():
            if node_id != node.id:
                raise ValueError(
                    f"Node dictionary key '{node_id}' does not match node id '{node.id}'."
                )

        for connection_id, connection in self.connections.items():
            if connection_id != connection.id:
                raise ValueError(
                    "Connection dictionary key "
                    f"'{connection_id}' does not match connection id '{connection.id}'."
                )

        for link_id, link in self.links.items():
            if link_id != link.id:
                raise ValueError(
                    f"Link dictionary key '{link_id}' does not match link id '{link.id}'."
                )

            self._validate_link_references(link)

    def _validate_link_references(self, link: Link) -> None:
        """Validate that a link references existing nodes and connection."""
        if link.connection_id not in self.connections:
            raise ValueError(
                f"Link '{link.id}' references unknown connection "
                f"'{link.connection_id}'."
            )

        if link.from_node_id not in self.nodes:
            raise ValueError(
                f"Link '{link.id}' references unknown from_node "
                f"'{link.from_node_id}'."
            )

        if link.to_node_id not in self.nodes:
            raise ValueError(
                f"Link '{link.id}' references unknown to_node "
                f"'{link.to_node_id}'."
            )

    # ------------------------------------------------------------------
    # Add objects
    # ------------------------------------------------------------------

    def add_node(self, node: Node) -> None:
        """Add a node to the system."""
        if not isinstance(node, Node):
            raise TypeError("Expected a Node object.")

        if node.id in self.nodes:
            raise ValueError(f"Node id '{node.id}' already exists.")

        self.nodes[node.id] = node

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the system."""
        if not isinstance(connection, Connection):
            raise TypeError("Expected a Connection object.")

        if connection.id in self.connections:
            raise ValueError(f"Connection id '{connection.id}' already exists.")

        self.connections[connection.id] = connection

    def add_link(self, link: Link) -> None:
        """Add a topological link to the system."""
        if not isinstance(link, Link):
            raise TypeError("Expected a Link object.")

        if link.id in self.links:
            raise ValueError(f"Link id '{link.id}' already exists.")

        self._validate_link_references(link)

        self.links[link.id] = link

    def connect(
        self,
        connection_id: str,
        from_node_id: str,
        to_node_id: str,
        link_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Link:
        """
        Create and add a link between a connection and two nodes.
        """
        link_kwargs: dict[str, Any] = {
            "connection_id": connection_id,
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "metadata": {} if metadata is None else dict(metadata),
        }

        if link_id is not None:
            link_kwargs["id"] = link_id

        link = Link(**link_kwargs)
        self.add_link(link)

        return link

    # ------------------------------------------------------------------
    # Get objects
    # ------------------------------------------------------------------

    def get_node(self, node_id: str) -> Node:
        """Return node by id."""
        return self.nodes[node_id]

    def get_connection(self, connection_id: str) -> Connection:
        """Return connection by id."""
        return self.connections[connection_id]

    def get_link(self, link_id: str) -> Link:
        """Return link by id."""
        return self.links[link_id]

    # ------------------------------------------------------------------
    # Node groups
    # ------------------------------------------------------------------

    def fixed_head_node_ids(self) -> list[str]:
        """Return ids of fixed-head nodes."""
        return [
            node_id
            for node_id, node in self.nodes.items()
            if node.is_fixed_head()
        ]

    def unknown_head_node_ids(self) -> list[str]:
        """Return ids of unknown-head nodes."""
        return [
            node_id
            for node_id, node in self.nodes.items()
            if node.is_unknown_head()
        ]

    def initial_unknown_heads(self) -> list[float]:
        """Return initial guesses for unknown-head nodes."""
        return [
            self.nodes[node_id].initial_head()
            for node_id in self.unknown_head_node_ids()
        ]

    # ------------------------------------------------------------------
    # Hydraulic evaluation helpers
    # ------------------------------------------------------------------

    def heads_from_unknowns(
        self,
        unknown_heads: list[float] | tuple[float, ...],
        alpha: float = 1.0,
    ) -> dict[str, float]:
        """
        Build a complete node-head dictionary from unknown-head values.

        Fixed-head nodes are filled using node.fixed_head(alpha).
        Unknown-head nodes are filled from the supplied vector.
        """
        unknown_node_ids = self.unknown_head_node_ids()

        if len(unknown_heads) != len(unknown_node_ids):
            raise ValueError(
                "Number of unknown head values does not match number of "
                "unknown-head nodes."
            )

        heads: dict[str, float] = {}

        for node_id, node in self.nodes.items():
            if node.is_fixed_head():
                heads[node_id] = node.fixed_head(alpha)

        for node_id, head in zip(unknown_node_ids, unknown_heads):
            heads[node_id] = float(head)

        return heads

    def link_delta_h(self, link_id: str, heads: dict[str, float]) -> float:
        """
        Return delta_h across a link.

        Convention:
            delta_h = H_to - H_from
        """
        link = self.get_link(link_id)

        h_from = float(heads[link.from_node_id])
        h_to = float(heads[link.to_node_id])

        return h_to - h_from

    def link_flow_rate(self, link_id: str, heads: dict[str, float]) -> float:
        """
        Return signed flow rate through a link.

        Convention:
            q > 0 means flow from from_node_id to to_node_id.
        """
        link = self.get_link(link_id)
        connection = self.get_connection(link.connection_id)

        delta_h = self.link_delta_h(link_id, heads)

        return connection.flow_rate(delta_h)

    def all_link_flow_rates(self, heads: dict[str, float]) -> dict[str, float]:
        """Return signed flow rate for every link."""
        return {
            link_id: self.link_flow_rate(link_id, heads)
            for link_id in self.links
        }

    # ------------------------------------------------------------------
    # Residual assembly
    # ------------------------------------------------------------------

    def nodal_flow_residuals(
        self,
        unknown_heads: list[float] | tuple[float, ...],
        alpha: float = 1.0,
    ) -> list[float]:
        """
        Assemble mass-balance residuals for unknown-head nodes.

        Residual convention:

            residual = external_flow + inflow_from_links - outflow_to_links

        For each link:
            q > 0 from from_node to to_node

            contribution to from_node = -q
            contribution to to_node   = +q

        At solution:
            residual = 0
        """
        heads = self.heads_from_unknowns(unknown_heads, alpha)
        residual_by_node = {
            node_id: self.nodes[node_id].external_flow(alpha)
            for node_id in self.unknown_head_node_ids()
        }

        for link_id, link in self.links.items():
            q = self.link_flow_rate(link_id, heads)

            if link.from_node_id in residual_by_node:
                residual_by_node[link.from_node_id] -= q

            if link.to_node_id in residual_by_node:
                residual_by_node[link.to_node_id] += q

        return [
            residual_by_node[node_id]
            for node_id in self.unknown_head_node_ids()
        ]

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert the system to a serializable dictionary."""
        return {
            "id": self.id,
            "nodes": [
                node.to_dict()
                for node in self.nodes.values()
            ],
            "connections": [
                connection.to_dict()
                for connection in self.connections.values()
            ],
            "links": [
                link.to_dict()
                for link in self.links.values()
            ],
            "metadata": self.metadata,
        }
from typing import Dict, List, Set
from graphbook.graph.node import Node
import uuid


class Graph:
    tags: Dict[str, Set[str]]
    nodes: Dict[str, Node]  # TODO: reconsider whether this should be in a Graph.
    id: str

    __slots__ = ["links", "tags", "nodes", "id"]

    def __init__(self) -> None:
        """A Graph is initialised as an empty set of Nodes, tags."""
        self.tags = {}
        self.nodes = {}
        self.id = str(uuid.uuid4())

    # I originally wanted to have another method called link_id that
    # would take a pair of strings, but that doesn't let me add the
    # node ID in.  I haven't thought through the implications of
    # adding a link to a node that the graph doesn't know about.
    def link(self, node1: Node, node2: Node) -> None:
        if not node1.id in self.nodes:
            self.add_node(node1)

        if not node2.id in self.nodes:
            self.add_node(node2)

        node1.link(node2.id)
        node2.link(node1.id)

    def add_node(self, node: Node) -> None:
        """Add Node to the Graph, subsuming its tags."""
        self.nodes[node.id] = node
        for tag in node.tags:
            if not tag in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(node.id)

    def tagged_nodes(self, tag: str) -> List[str]:
        node_ids = []
        for node_id in self.nodes:
            if self.nodes[node_id].is_tagged(tag):
                node_ids.append(node_id)
        return node_ids

    def tag_list(self) -> List[str]:
        """Get a list of all the tags in the Graph."""
        tags: Set[str] = set()
        for node_id in self.nodes:
            # Q: should a node have a tag_set function?
            tags.update(self.nodes[node_id].tags)
        return sorted(list(tags))

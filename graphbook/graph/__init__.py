from __future__ import annotations  # need to return Cell from Cell
from typing import Counter, Dict, List, Set
import collections
import uuid


def __decode_text__(s, codec="utf-8"):
    return s.decode(codec)


class Cell:
    """
    A Cell is smallest piece of a Node. This implementation of a cell
    is a basic, plaintext version, with no additional rendering.
    """

    # Everything in graphbook gets a UUID, because it seems to be cheap
    # and having a unique identifier could be useful later.
    id: str

    # The contents of a cell should just be bytes. This lets you shove
    # anything in them, and leave it up to the UI to render.
    contents: bytes

    def __init__(self, contents: bytes) -> None:
        self.id = str(uuid.uuid4())
        self.contents = contents

    def render(self, decoder=__decode_text__) -> str:
        return decoder(self.contents)

    def execute(self) -> str:
        return ""

    def dup(self) -> Cell:
        return Cell(self.contents)


class Node:
    id: str
    cells: List[Cell]
    links: Counter[str]

    # probably useful too: tags, metadata... need to think about how
    # to make metadata useful; str->str isn't super useful (or gets
    # that way quickly), but str->any is too open ended. What's the
    # Goldilocks type?

    __slots__ = ["id", "cells", "links"]

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.cells = []
        self.links = collections.Counter()

    def add(self, cell: Cell) -> str:
        self.cells.append(cell)
        return cell.id

    def render_all(self) -> str:
        rendered = ""
        for cell in self.cells:
            rendered += cell.render()
        return rendered

    # Linking is tricky. Who should know about the relationship
    # between two nodes? When I started out writing this, it seemed
    # obvious that the links should go in a graph. Now I think nodes
    # should keep the linking information, and the graph should just
    # be a collection of nodes (and optionally tags).
    #
    # Another related thought is that maybe I need to make a link type
    # that lets you specify the namespace and unique ID of the
    # node. This brings up a bunch of questions, like should these
    # links get their own separate ID, and what do we do with them?
    # They could be like capabilities, but then you have to query the
    # node for it and it starts getting mushy. I need to spend some
    # more time thinking about this.
    def link(self, node_id: str) -> None:
        """link adds the node_id to the list of links for the node."""
        self.links[node_id] += 1


class Graph:
    tags: Dict[str, Set[str]]
    nodes: Dict[str, Node]
    namespace: str

    __slots__ = ["links", "tags", "nodes", "namespace"]

    def __init__(self) -> None:
        self.tags = {}
        self.nodes = {}
        self.namespace = str(uuid.uuid4())

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
        self.nodes[node.id] = node

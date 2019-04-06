# This import allows specifying the class being defined as the return
# type.
from __future__ import annotations

from typing import List, Set
from graphbook.graph.cell import Cell
import uuid


class Node:
    id: str
    cells: List[Cell]
    links: Set[str]
    tags: Set[str]

    # probably useful too: tags, metadata... need to think about how
    # to make metadata useful; str->str isn't super useful (or gets
    # that way quickly), but str->any is too open ended. What's the
    # Goldilocks type?

    __slots__ = ["id", "cells", "links", "tags"]

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.cells = []
        self.links = set()
        self.tags = set()

    def add(self, cell: Cell) -> str:
        """Append a Cell to this Node."""
        self.cells.append(cell)
        return cell.id

    def render_all(self) -> str:
        """Render all Cells in this Node."""
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
        self.links.add(node_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        # Two equal nodes must have the same ID.
        if self.id != other.id:
            return False

        # Two equal nodes have the same cells.
        if len(self.cells) != len(other.cells):
            return False

        for i, cell in enumerate(self.cells):
            if cell != other.cells[i]:
                return False

        # Two equal nodes have the same links.
        if self.links != other.links:
            return False

        # Two equal nodes have the same tags.
        if self.tags != other.tags:
            return False

        return True

    # TODO: how to communicate tag changes to a graph?

    def is_tagged(self, tag: str) -> bool:
        """Return True if this node has been tagged with `tag`."""
        return tag in self.tags

    def tag(self, tag: str) -> None:
        """Add a tag to this node."""
        self.tags.add(tag)

    def untag(self, tag: str) -> None:
        """Remove a tag from this node."""
        if tag in self.tags:
            self.tags.remove(tag)

# -*- coding: utf-8 -*-
"""
Nodes serve as pages in a notebook. They're a list of cells, along with
links and other metadata.
"""
from __future__ import annotations
import graphbook.graph.cell as cell
from typing import List, Optional, Set
from uuid import uuid4


class Node:
    """
    Nodes serve as pages in a notebook. They're a list of cells, along with
    links to other nodes.
    """

    id: str
    title: str
    cells: List[cell.Cell]
    links: Set[str]
    tags: Set[str]

    def __init__(self, title: str) -> None:
        """Initialise a blank cell, generating a new random ID."""
        self.id = str(uuid4())
        self.title = title
        self.cells = []
        self.links = set()
        self.tags = set()

    def add(self, cell: cell.Cell) -> None:
        """Append cell to this node's cell list."""
        self.cells.append(cell)

    def remove(self, index: Optional[int] = None) -> None:
        """Remove the cell at the given index."""
        if index is not None:
            self.cells = self.cells[:index] + self.cells[index + 1 :]

    def insert(self, cell: cell.Cell, index: int):
        """Insert cell at the given index."""
        self.cells.insert(index, cell)

    def to_obj(self):
        """Return a dictionary of the node suitable for serialising."""
        return {
            "id": self.id,
            "title": self.title,
            "links": list(self.links),
            "cells": [c.to_obj() for c in self.cells],
            "tags": list(self.tags),
        }

    def link(self, node: Node) -> None:
        """Register a link to another node."""
        self.links.add(node.id)

    @classmethod
    def from_obj(cls, obj):
        """Parse ``obj`` as a node."""
        if "id" not in obj:
            raise (ValueError("object isn't a Node: missing id"))
        if "title" not in obj:
            raise (ValueError("object isn't a Node: missing title"))
        if "links" not in obj:
            raise (ValueError("object isn't a Node: missing links"))

        n = cls(obj["title"])
        n.id = obj["id"]
        n.links = set(obj["links"])
        if "cells" in obj:
            n.cells = [cell.load_cell(cobj) for cobj in obj["cells"]]

        if "tags" in obj:
            n.tags = set(obj["tags"])

        return n

    def tag(self, tag: str) -> None:
        """Add a tag to this node."""
        self.tags.add(tag)

    def untag(self, tag: str) -> None:
        """Remove a tag from this node."""
        if tag in self.tags:
            self.tags.remove(tag)

    def render(self) -> str:
        """Render all the nodes."""
        return "\n\n".join([c.render() for c in self.cells])

    # node is subscriptable and supports equality checking.

    def __getitem__(self, i: int) -> cell.Cell:
        return self.cells[i]

    def __setitem__(self, i: int, c: cell.Cell):
        self.cells[i] = c

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.id != other.id:
            return False

        if self.title != other.title:
            return False

        if self.links != other.links:
            return False

        if len(self.cells) != len(other.cells):
            return False

        for i in range(len(self.cells)):
            if self.cells[i] != other.cells[i]:
                return False

        if self.tags != other.tags:
            return False

        return True

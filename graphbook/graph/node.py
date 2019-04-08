# -*- coding: utf-8 -*-
"""
Nodes serve as pages in a notebook. They're a list of cells, along with
links and other metadata.
"""

import graphbook.graph.cell as cell
from typing import List, Optional, Set
from uuid import uuid4

class Node:
    """
    Nodes serve as pages in a notebook. They're a list of cells, along with
    links to other nodes.
    """
    id: str
    cells: List[cell.Cell]
    links: Set[str]

    def __init__(self) -> None:
        """Initialise a blank cell, generating a new random ID."""
        self.id = str(uuid4())
        self.cells = []
        self.links = set()

    def add(self, cell: cell.Cell) -> None:
        """Append cell to this node's cell list."""
        self.cells.append(cell)

    def remove(self, index: Optional[int] = None) -> None:
        """Remove the cell at the given index."""
        if index:
            self.cells = self.cells[:index] + self.cells[index + 1 :]

    def insert(self, Cell: cell.Cell, index: int):
        """Insert cell at the given index."""
        pass

    def to_obj(self):
        """Return a dictionary of the node suitable for serialising."""
        return {
            "id": self.id,
            "links": list(self.links),
            "cells": [c.to_obj() for c in self.cells],
        }

    @classmethod
    def from_obj(cls, obj):
        """Parse ``obj`` as a node."""
        if "id" not in obj:
            raise (ValueError("object isn't a Node: missing id"))
        if "links" not in obj:
            raise (ValueError("object isn't a TextCell: missing links"))

        n = cls()
        n.id = obj["id"]
        n.links = set(obj["links"])
        if "cells" in obj:
            n.cells = [cell.load_cell(cobj) for cobj in obj["cells"]]

        return n

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.id != other.id:
            return False

        if self.links != other.links:
            return False

        if len(self.cells) != len(other.cells):
            return False

        for i in range(len(self.cells)):
            if self.cells[i] != other.cells[i]:
                return False

        return True

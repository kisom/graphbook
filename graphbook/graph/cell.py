# -*- coding: utf-8 -*-
"""
The 'atom' of GraphBook is the Cell.
"""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Dict, Optional
from uuid import uuid4
import pdb


class Cell:
    """
    A Cell is just a mechanism for capturing some information, and pairs some
    binary content with a unique ID and a type. This superclass provides the
    content and ID, but subclasses must set the type.
    """

    id: str
    type: str
    contents: bytes

    def __init__(self, contents: bytes):
        """Initialising a Cell copies the contents into the cell and generates
        a new ID. Subclasses are responsible for implementing the type.
        """
        self.id = str(uuid4())
        self.contents = contents

    def render(self, decoder=None) -> str:
        """Return the contents of the cell suitable for display."""
        raise (NotImplementedError)

    def is_executable(self) -> bool:
        """Return True if this cell can be executed."""
        raise (NotImplementedError)

    def execute(self) -> str:
        """Return the results of executing this cell."""
        raise (NotImplementedError)

    def to_obj(self) -> Dict[str, str]:
        """Return a dictionary of the cell suitable for serialising."""
        raise (NotImplementedError)

    def dup(self) -> Cell:
        """Return a duplicate of this cell with a different ID."""
        new_cell = Cell(self.contents)
        new_cell.type = self.type
        return new_cell

    @classmethod
    def from_obj(cls, obj: Dict[str, str]) -> Cell:
        """Parse an object as a Cell."""
        raise (NotImplementedError)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.id != other.id:
            return False

        if self.contents != other.contents:
            return False

        if self.type != other.type:
            return False

        return True


__DEFAULT_ENCODING: str = "utf-8"


def _decode(contents: bytes, encoding: str = __DEFAULT_ENCODING) -> str:
    return contents.decode(encoding)


class TextCell(Cell):
    """
    TextCells store unformatted plain text, rendered as UTF-8.
    """

    def __init__(self, contents: bytes):
        super().__init__(contents)
        self.type = "text"

    def render(self, decoder=_decode) -> str:
        return decoder(self.contents)

    def is_executable(self) -> bool:
        return False

    def execute(self) -> str:
        return ""

    def to_obj(self):
        return {"id": self.id, "type": self.type, "contents": self.render()}

    @classmethod
    def from_obj(cls, obj: Dict[str, str]) -> TextCell:
        if not "type" in obj:
            raise (ValueError("object isn't a TextCell: missing type"))
        if not "contents" in obj:
            raise (ValueError("object isn't a TextCell: missing contents"))
        if not "id" in obj:
            raise (ValueError("object isn't a TextCell: missing id"))

        # using DEFAULT_ENCODING here doesn't work because scoping?
        cell = cls(obj["contents"].encode("utf-8"))
        cell.id = obj["id"]
        return cell


__REGISTRY: Dict[str, Cell] = {}


def register_cell_type(cell_type: str, cls, replace=False):
    global __REGISTRY

    if not cell_type in __REGISTRY or replace:
        __REGISTRY[cell_type] = cls


def load_cell(obj: Dict[str, str]) -> Optional[Cell]:
    if "type" not in obj:
        raise (TypeError("object isn't a Cell object"))

    if obj["type"] not in __REGISTRY:
        raise (KeyError("Unregistered type " + obj["type"]))

    return __REGISTRY[obj["type"]].from_obj(obj)


register_cell_type("text", TextCell)

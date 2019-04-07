"""
cell.py contains the definition of a cell; the base implementation
is a plaintext cell node.

A cell should have three methods:

+ render: ((str? -> str)? -> str) returns the rendered contents
  of the cell.
+ is_executable: () -> bool returns whether this node is executable.
+ execute: () -> str returns an empty string if the Cell is executable,
  or the output of executing the contents of the Cell.
"""
# This import allows specifying the class being defined as the return
# type of the cell.
from __future__ import annotations
from abcmeta import ABCMeta
from typing import Dict
import uuid

__DEFAULT_CODEC__: str = "utf-8"


def __decode_text__(s, codec=__DEFAULT_CODEC__):
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

    type: str

    __slots__ = ["id", "contents", "type"]

    def __init__(self, contents: bytes) -> None:
        """
        A Cell should be initialised with some contents, which is just
        a byte array.
        """

        self.id = str(uuid.uuid4())
        self.contents = contents
        self.type = ""

    def render(self, decoder=__decode_text__) -> str:
        """
        Return the rendered contents of the cell, with the option of specifying
        a decoder for the contents. This should be purely optional, and a Cell
        must be able to render something useful if no decoder is provided.
        """
        return decoder(self.contents)

    def is_executable(self) -> bool:
        """A plain Cell isn't executable."""
        return False

    def execute(self) -> str:
        """Execute the contents of the cell."""
        return ""

    def dup(self) -> Cell:
        """
        Duplicate the contents of this cell into a new Cell. This is provided to
        support copying and pasting cells; editing a duplicated Cell shouldn't
        change the contents of the original Cell.
        """
        return Cell(self.contents)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented

        """Two Cells are equal if they have the same id and contents."""
        if self.id != other.id:
            return False

        return self.contents == other.contents

    def dump(self) -> Dict[str, object]:
        """Return a dictionary that represents a cell."""

        # HACK: this makes it easier to edit nodes before the UI has usable editing support.
        return {
            "id": self.id,
            "type": self.type,
            "contents": self.contents.decode(__DEFAULT_CODEC__),
        }


__REGISTRY: Dict[str, object] = {"": Cell}


def register_type(kind: str, constructor: object) -> None:
    """Register a new typestring and the type it represents."""
    global __REGISTRY
    __REGISTRY[kind] = constructor


def load_cell(obj: Dict[str, object]) -> Cell:
    """load cell takes an object from Cell.dump() and turns it back into a cell."""

    constructor: object = Cell
    if "type" in obj and obj["type"] in __REGISTRY:
        constructor = __REGISTRY[str(obj["type"])]

    cell = constructor(obj["contents"].encode(__DEFAULT_CODEC__))
    cell.id = obj["id"]
    return cell

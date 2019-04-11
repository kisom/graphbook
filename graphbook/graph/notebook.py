# -*- coding: utf-8 -*-
"""
A Notebook is the top-level GraphBook abstraction.
"""

from __future__ import annotations
from collections import namedtuple
from typing import Any, Dict, Iterable, List, Optional, Set
import graphbook.graph.node as node
from graphbook.graph.serial import from_yaml, to_yaml
import os
from uuid import uuid4


class NodeEntry:
    """
    A NodeEntry contains metadata about a node that's useful for a
    frontend to use in place of a full node.
    """

    id: str
    title: str
    tags: List[str]
    links: List[str]

    def __init__(self, id: str, title: str, tags: Iterable[str], links: Iterable[str]):
        self.id = id
        self.title = title
        self.tags = list(tags)
        self.links = list(links)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        if self.id != other.id:
            return False

        if self.title != other.title:
            return False

        if self.tags != other.tags:
            return False

        if self.links != other.links:
            return False

        return True

    def __lt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id < other.id

    def to_obj(self) -> Dict[str, Any]:
        """Convert a ``NodeEntry`` to an object."""
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "links": self.links,
        }

    @classmethod
    def from_obj(cls, obj: Dict[str, Any]) -> NodeEntry:
        if "id" not in obj:
            raise (ValueError("object isn't a NodeEntry: missing id"))
        if "title" not in obj:
            raise (ValueError("object isn't a NodeEntry: missing title"))
        if "tags" not in obj:
            raise (ValueError("object isn't a NodeEntry: missing tags"))
        if "links" not in obj:
            raise (ValueError("object isn't a NodeEntry: missing links"))

        return NodeEntry(obj["id"], obj["title"], obj["tags"], obj["links"])


class Notebook:
    """A Notebook points to a directory of Nodes."""

    id: str
    path: str
    abspath: str
    tags: Dict[str, Set[str]]
    nodes: Dict[str, NodeEntry]

    def __init__(self, path: str = "graphbook") -> None:
        self.id = str(uuid4())
        self.path = path
        self.abspath = os.path.abspath(self.path) + os.sep
        self.tags = {}
        self.nodes = {}
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.scan()

    def _is_maybe_node(self, path: str) -> bool:
        # Extension seems like a weak approach but it simplifies things for now.
        full_path = os.path.abspath(os.path.join(self.path, path))
        if not path.endswith("node"):
            return False
        if not os.path.isfile(full_path):
            return False
        return True

    def scan(self) -> int:
        """Rebuild the internal caches by scanning the notebook directory."""
        self.tags = {}
        self.nodes = {}

        listing = os.listdir(self.path)
        nodes: List[str] = [
            os.path.join(self.path, path)
            for path in listing
            if self._is_maybe_node(path)
        ]

        for node_path in nodes:
            self._noder(node_path)

        return len(nodes)

    def noder(self, node_id) -> Optional[node.Node]:
        """
        Read the node with the given node ID from disk. This will also update the
        internal caches as necessary.
        """
        node_path = os.path.join(self.abspath, node_id) + ".node"
        return self._noder(node_path)

    def _noder(self, node_path: str) -> Optional[node.Node]:
        try:
            with open(node_path, "rt") as node_file:
                nobj = from_yaml(node_file.read())
        except FileNotFoundError:
            return None

        _node = node.Node.from_obj(nobj)
        self._update_node(_node)
        return node.Node.from_obj(nobj)

    def nodew(self, _node: node.Node) -> None:
        """
        Write the node to disk. This will update the internal caches as necessary.
        """
        self._update_node(_node)
        nobj = _node.to_obj()
        with open(os.path.join(self.path, _node.id + ".node"), "wt") as node_file:
            node_file.write(to_yaml(nobj))

    def _update_node(self, _node: node.Node) -> None:
        self.nodes[_node.id] = NodeEntry(_node.id, _node.title, _node.tags, _node.links)
        for tag in _node.tags:
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(tag)

    def select(
        self, text: str = "", cased: bool = False, and_tags: Optional[List[str]] = None
    ) -> List[NodeEntry]:
        """
        Return the list of titles for all nodes; if text is not empty, nodes whose
        titles start with or contain text will be returned.
        """
        startswith: List[NodeEntry] = []
        contains: List[NodeEntry] = []

        print("text:", text)
        if text == "":
            startswith = sorted(self.nodes.values())
        else:
            if not cased:
                text = text.lower()

            for n in self.nodes.values():
                title: str = n.title
                if not cased:
                    title = n.title.lower()
                if title.startswith(text):
                    startswith.append(n)
                elif text in title:
                    contains.append(n)

            startswith.extend(contains)

        if and_tags:
            tagset: Set[str] = set(and_tags)
            startswith = [
                nentry for nentry in startswith if tagset.issubset(nentry.tags)
            ]
        return startswith

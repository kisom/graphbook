# -*- coding: utf-8 -*-
"""
A Notebook is a graph and some additional metadata.
"""

from collections import namedtuple
from typing import Dict, List, Optional, Set
import graphbook.graph.node as node
from graphbook.graph.serial import from_yaml, to_yaml
import os
from uuid import uuid4


NodeEntry = namedtuple("NodeEntry", ("id", "title", "tags", "links"))


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
        self._update_node(_node)
        nobj = _node.to_obj()
        with open(os.path.join(self.path, _node.id), "wt") as node_file:
            node_file.write(to_yaml(nobj))

    def _update_node(self, _node: node.Node) -> None:
        self.nodes[_node.id] = NodeEntry(_node.id, _node.title, _node.tags, _node.links)
        for tag in _node.tags:
            if tag not in self.tags:
                self.tags[tag] = set()
            self.tags[tag].add(tag)

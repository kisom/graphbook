# -*- coding: utf-8 -*-
"""
A Notebook is a graph and some additional metadata.
"""

from typing import Dict, Set
import graphbook.graph.node as node
from uuid import uuid4


class Graph:
    id: str
    nodes: Dict[str, node.Node]
    tags: Dict[str, Set[str]]
    # IDEA: could add a related links structure that maps a tag to a
    # counter of related tags.

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.nodes = {}
        self.tags = {}

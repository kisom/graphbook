from typing import Dict, List, Set
import uuid


class Cell:
    id: str
    contents: bytes
    codec: str = 'utf-8'

    def __init__(self, contents: bytes) -> None:
        self.id = str(uuid.uuid4())
        self.contents = contents

    def render(self) -> str:
        return self.contents.decode(self.codec)

    def dup(self) -> Cell:
        return Cell(self.contents)


class Node:
    id: str
    cells: List[Cell]

    # probably useful too: tags, metadata... need to think about how
    # to make metadata useful; str->str isn't super useful (or gets
    # that way quickly), but str->any is too open ended. What's the
    # Goldilocks type?
    
    __slots__ = ['id', 'cells']
    
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.cells = []

    def add(self, cell: Cell) -> str:
        self.cells.append(cell)


class Graph:
    links: Dict[str, Set[str]]
    tags: Dict[str, Set[str]]
    nodes: Dict[str, Node]
    namespace: str

    __slots__ = ['links', 'tags', 'nodes', 'namespace']
    
    def __init__(self) -> None:
        self.links = {}
        self.tags = {}
        self.nodes = {}
        self.namespace = str(uuid.uuid4())

    def link(self, node1: Node, node2: Node) -> None:
        if not node1.id in self.nodes:
            self.add_node(node1)

        if not node2.id in self.nodes:
            self.add_nodes(node2)

        self.link_id(node1.id, node2.id)

    def link_id(self, node1: str, node2: str) -> None:
        if not node1 in self.links:
            self.links[node1] = set()
        if not node2 in self.links:
            self.links[node2] = set()

        self.links[node1].add(node2)
        self.links[node2].add(node1)

    def add_node(self, node: Node) -> str:
        self.nodes[node.id] = node
        return node.id

# -*- coding: utf-8 -*-

from context import cell, node
import yaml

n1 = None

def test_node():
    global n1
    n1 = node.Node()
    cells = [b'hello world', b'goodbye, world', b'text of a textual nature']
    cells = list(map(cell.TextCell, cells))
    for c in cells:
        n1.add(c)

    n1.tag("test")
    n1.tag("world")

    assert(len(n1.cells) == len(cells))
    nobj = n1.to_obj()
    n2 = node.Node.from_obj(nobj)
    assert(n1 == n2)

def test_node_yaml():
    nobj = n1.to_obj()
    nser = yaml.dump(nobj)
    n2 = node.Node.from_obj(yaml.load(nser))
    assert(n1 == n2)

def test_remove():
    cells = n1.cells
    n1.cells = [1, 2, 3]
    n1.remove(2)
    assert(1 in n1.cells)
    assert(2 in n1.cells)

    n1.remove(0)
    assert(2 in n1.cells)
    n1.remove()
    assert(2 in n1.cells)
    n1.remove(0)
    assert(len(n1.cells) == 0)

    n1.cells = cells

def test_insert():
    cells = n1.cells
    n1.cells = [1, 2, 3]
    n1.insert(42, 0)

    assert(n1.cells[0] == 42)

    n1.insert(37, 3)
    assert(n1.cells[3] == 37)

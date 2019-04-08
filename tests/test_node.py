# -*- coding: utf-8 -*-

from context import cell, node


def test_node():
    n1 = node.Node()
    cells = [b'hello world', b'goodbye, world', b'text of a textual nature']
    cells = list(map(cell.TextCell, cells))
    for c in cells:
        n1.add(c)

    assert(len(n1.cells) == len(cells))
    nobj = n1.to_obj()
    n2 = node.Node.from_obj(nobj)
    assert(n1 == n2)
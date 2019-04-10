# -*- coding: utf-8 -*-

from context import cell, node, notebook
import os
import shutil
import tempfile

demobook = notebook.Notebook("tests/demobook")


def test_demobook():
    assert(len(demobook.nodes) == 3)
    assert(len(demobook.nodes) == len(demobook.select()))
    results = demobook.select('graph')
    assert(len(results) == 2)

    node_ids = list(demobook.nodes.keys())
    _node = demobook.noder(node_ids[0])
    assert(_node.id == node_ids[0])

def test_newnotebook():
    try:
        fd, tempdir = tempfile.mkstemp()
        os.close(fd)
        os.unlink(tempdir)

        nb = notebook.Notebook(tempdir)
        _node = node.Node("A notebook of tests and possibilities")
        _node.add(cell.TextCell(b"Hacks and glory await!"))

        nb.nodew(_node)
        assert(nb.scan() == 1)

    finally:
        shutil.rmtree(tempdir)
    

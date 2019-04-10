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

    assert(len(demobook.select('', and_tags=['node'])) < len(demobook.nodes))

def test_is_maybe_path():
    assert(not(demobook._is_maybe_node('node-a-node')))
    assert(not(demobook._is_maybe_node('not-a' +'.node')))
    assert(demobook.noder('not-a-node') is None)
    
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
    
def test_nodeentry():
    nentry = demobook.select()[0]
    assert(notebook.NodeEntry.from_obj(nentry.to_obj()) == nentry)

# -*- coding: utf-8 -*-

from context import notebook, to_yaml, from_yaml

demobook = notebook.Notebook("tests/demobook")

def test_demobook():
    assert(len(demobook.nodes) == 3)
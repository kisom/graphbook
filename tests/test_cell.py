# -*- coding: utf-8 -*-

from context import cell, to_yaml, from_yaml

def test_cell():
    print('[+] constructing cell')
    c1 = cell.TextCell(b'hello, world')

    print('[+] objectifying cell')
    cobj = c1.to_obj()

    print('[+] unobjectifying cell')
    c2 = cell.load_cell(cobj)

    print('[+] assert!' )
    assert(c1 == c2)

    print("HOKAY")

def test_cell_yaml():
    c1 = cell.TextCell(b'hello, world')
    cobj = c1.to_obj()
    cser = to_yaml(cobj)
    c2 = cell.load_cell(from_yaml(cser))
    assert(c1 == c2)

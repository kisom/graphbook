# -*- coding: utf-8 -*-

from context import cell, to_yaml, from_yaml
import pytest

def test_cell():
    print('[+] constructing cell')
    c1 = cell.TextCell(b'hello, world')
    assert(not(c1.is_executable()))

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

    c3 = c1.dup()
    assert(c1 != c3)

def test_load_cell():
    c1 = cell.TextCell(b'hello, world')
    cobj = c1.to_obj()

    del(cobj['type'])
    with pytest.raises(TypeError):
        cell.load_cell(cobj)

    cobj['type'] = 'unsupported'
    with pytest.raises(KeyError):
        cell.load_cell(cobj)

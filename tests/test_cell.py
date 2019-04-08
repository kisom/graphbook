# -*- coding: utf-8 -*-

import yaml
from context import cell

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
    cser = yaml.dumps(cobj)
    c2 = cell.load_cell(yaml.loads(cser))
    assert(c1 == c2)
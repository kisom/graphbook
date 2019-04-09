# -*- coding: utf-8 -*-
"""
vm contains various implementations of executable cells.
"""

from graphbook.vm import uscheme
from graphbook.graph import cell

cell.register_cell_type("uscheme", uscheme.MicroSchemeCell)

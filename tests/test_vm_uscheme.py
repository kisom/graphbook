# -*- coding: utf-8 -*-

from context import uscheme

def test_uscheme_cell():
    program = """
(define square (lambda (x) (* x x)))
(define circle-area (lambda (r) (* pi (square r))))
(circle-area 3)
"""
    program_bytes = program.encode('utf-8')
    cell = uscheme.MicroSchemeCell(program_bytes)
    assert(cell.render() == program)
    assert(cell.is_executable())
    assert(cell.execute() == "28.274333882308138")
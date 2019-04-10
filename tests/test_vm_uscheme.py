# -*- coding: utf-8 -*-

from context import cell

def test_uscheme_cell():
    program = """
(define square (lambda (x) (* x x)))
(define circle-area (lambda (r) (* pi (square r))))
(define r 3)
(if (> r 5)
    r
    (circle-area 3))
"""
    program_bytes = program.encode('utf-8')
    uscheme_cell = cell.MicroSchemeCell(program_bytes)
    assert(uscheme_cell.render() == program)
    assert(uscheme_cell.is_executable())
    assert(uscheme_cell.execute() == "28.274333882308138")

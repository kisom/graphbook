# -*- coding: utf-8 -*-

from context import cell, uscheme
import os, tempfile

def test_uscheme_cell():
    program = """
(define square (lambda (x) (* x x)))
(define circle-area (lambda (r) (* pi (square r))))
(define r 3)
(define x (quote 2))
(if (> r 5)
    r
    (circle-area 3))
"""
    program_bytes = program.encode('utf-8')
    uscheme_cell = cell.MicroSchemeCell(program_bytes)
    assert(uscheme_cell.render() == program)
    assert(uscheme_cell.is_executable())
    assert(uscheme_cell.execute() == "28.274333882308138")

def test_uscheme_load_file():
    program = """
(define square (lambda (x) (* x x)))
(define circle-area (lambda (r) (* pi (square r))))
(define r 3)
(define x (quote 2))
(if (> r 5)
    r
    (circle-area 3))
"""
    fd, tfile = tempfile.mkstemp(suffix='.scm', text=True)
    os.write(fd, program.encode('utf-8'))
    os.close(fd)

    try:
        interpreter = uscheme.Interpreter()
        result = interpreter.load_file(tfile)
        assert(result == 28.274333882308138)
    finally:
        os.remove(tfile)

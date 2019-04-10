# -*- coding: utf-8 -*-
"""
uscheme implements a microscheme from Peter Norvig's lis.py - this
is the more primitive of the two versions. This isn't a full Scheme,
and in particular has the following caveats:

1. The only types are symbols, ints, and floats.
2. Function definition must be done via ``(define func (lambda ...))``;
   doing ``(define func ...)`` will result in an error.

"""

# Caveat emptor: this is a mostly untyped file, as I haven't figured out
# how to reconcile some of the Scheme way with the typed way.

from collections import ChainMap as Environment
from collections import namedtuple
from typing import Any, Dict, List, Optional

import math
import operator as op
import sys

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list  # type: ignore
Exp = (Atom, List)


def tokenise(expr):
    return expr.replace("(", " ( ").replace(")", " ) ").split()


def atom(token: str) -> Atom:  # type: ignore
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def expression_from_tokens(tokens: list) -> Exp:  # type: ignore
    """Given a list of tokens, return the first expression that was found."""
    if not tokens:
        raise SyntaxError("unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L: List[Exp] = []  # type: ignore
        while tokens[0] != ")":
            L.append(expression_from_tokens(tokens))
        tokens.pop(0)  # remove trailing paren
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def standard_env():
    """Return the standard environment."""
    env = {}
    env.update(vars(math))

    scrub_keys = [
        "__name__",
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__file__",
    ]
    for key in scrub_keys:
        env.pop(key, None)

    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": lambda proc, args: proc(*args),
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": lambda *x: list(x),
            "list?": lambda x: isinstance(x, list),
            "map": lambda *args: list(map(*args)),
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, Number),
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        }
    )

    return env


def eval(exp, env):
    "Evaluate an expression in an environment."
    if isinstance(exp, Symbol):
        return env[exp]
    elif not isinstance(exp, List):
        return exp
    elif exp[0] == "quote":
        return exp[1:]
    elif exp[0] == "if":
        (_, cond, texp, fexp) = exp
        if eval(cond, env):
            return eval(texp, env)
        return eval(fexp, env)
    elif exp[0] == "define":
        (_, var, _exp) = exp
        env[var] = eval(_exp, env)
    elif exp[0] == "lambda":
        (_, params, body) = exp
        return Procedure(params, body, env)
    else:
        proc = eval(exp[0], env)
        args = [eval(arg, env) for arg in exp[1:]]
        return proc(*args)


class Procedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        env = Environment(dict(zip(self.params, args)), self.env)
        return eval(self.body, env)


class Interpreter:
    """
    A microscheme interpreter that maintains its own environment across runs.
    """

    def __init__(self, program: Optional[str] = None) -> None:

        """
        Intialise the environment with the standard environment.

        If ``scrub_keys`` is present, it is a list of names from the standard
        environment that should be dropped.

        If ``extra_env`` is present, it should be a dictionary of names to Symbols
        that should be added to the initial environment.

        If ``program`` is present, it is a program that will be evaluated after
        setting up the environment.
        """
        self.reset()
        # if program:
        #     self.eval(program)

    def reset(self):
        """reset the interpreter's environment to the standard env."""
        self.env = standard_env()

    def eval(self, program: str) -> Exp:  # type: ignore
        """evaluate a microscheme program."""
        tokens = tokenise(program)
        result = None
        while tokens:
            expr = expression_from_tokens(tokens)  # type: ignore
            result = eval(expr, self.env)
        if result is None:
            return ""
        return result

    def load_file(self, path):
        """load the microscheme source file at path and evaluate it."""
        with open(path, "rt") as pgm_file:
            return self.eval(pgm_file.read())


def standalone(paths) -> Any:
    """Standalone interpreter that will be run across the paths presented."""
    interpreter = Interpreter()
    result = None
    for path in paths:
        sys.stdout.write(path + ": ")
        result = interpreter.load_file(path)
        print(result)
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        standalone(sys.argv[1:])

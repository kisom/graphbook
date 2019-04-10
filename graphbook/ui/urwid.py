# -*- coding: utf-8 -*-

import graphbook.graph as graph
import argparse
import urwid  # type: ignore # urwid doesn't have type annotations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="graphbook", description="A programmer's knowledge repository"
    )
    parser.add_argument("path", help="The path to the GraphBook")
    args = parser.parse_args()

# -*- coding: utf-8 -*-

import argparse
import curses
import os
import pdb
import sys
import textwrap
import graphbook.graph as graph
import graphbook.vm.uscheme as uscheme
from typing import Any, Dict

active_node = None
selected_node = None
search_mode = False
search_buffer = ""
search_index = 0


class KeyMap:
    _keymap: Dict[int, Any]  # TODO: not sure what the function prototype for this is

    def __init__(self):
        self._keymap = {}

    def register(self, key, func):
        print("registered: ", key)
        if isinstance(key, str):
            key = ord(key)
        self._keymap[key] = func

    def press(self, key, scr, *args):
        if isinstance(key, str):
            key = ord(key)
        func = self._keymap.get(key, None)
        if not func:
            return None
        return func(scr, key, *args)


def render_cell(c: graph.cell.Cell, scr: Any) -> None:
    if c.is_executable():
        pass


def main(stdscr, args):
    global active_node
    global selected_node
    global search_mode
    global search_buffer
    global search_index

    notebook = graph.notebook.Notebook(args.path)
    pdb.set_trace()

    # Probably want to do this outside the function so we don't have
    # to rebuild on each function invocation.

    def fine_python(scr, *args):
        global search_mode
        search_mode = True

    kmap = KeyMap()
    kmap.register("/", fine_python)
    kmap.register("q", lambda scr, key: sys.exit(0))
    kmap.register

    while True:
        if not search_mode:
            if active_node:
                _node = notebook.noder(active_node)
                # Need a page type, but for now this works.
                stdscr.clear()
                stdscr.addstr("Node: {}\n".format(_node.title))
                stdscr.addstr("-----\n")

                for cell in _node.cells:
                    stdscr.addstr("\n")
                    lines = textwrap.wrap(cell.render(), 60)
                    for line in lines:
                        stdscr.addstr(line + "\n")

            c = stdscr.getch()
            kmap.press(c, stdscr)

        if search_mode:
            stdscr.addstr("> Search: " + search_buffer + "\n")
            nodes = notebook.titles(search_buffer)
            stdscr.addstr("  " + "\n  ".join([node.title for node in nodes]) + "  \n")
            stdscr.addstr(search_index + 1, 0, "+")
            c = stdscr.getch()
            stdscr.clear()

            if c == curses.KEY_ENTER or c == 27 or c == 0xA:
                search_mode = False
                search_buffer = ""
                if c == curses.KEY_ENTER or c == 0xA:
                    active_node = selected_node
                continue
            if c == curses.KEY_BACKSPACE:
                search_buffer = search_buffer[:-1]
            elif nodes and c == curses.KEY_UP:
                search_index -= 1
                search_index = search_index % len(nodes)
            elif nodes and c == curses.KEY_DOWN:
                search_index += 1
                search_index = search_index % len(nodes)
            elif chr(c).isalpha() or c == 0x20:
                search_buffer += chr(c)
            selected_node = nodes[search_index].id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="graphbook", description="A programmer's knowledge repository"
    )
    parser.add_argument("path", help="The path to the GraphBook")
    args = parser.parse_args()
    curses.wrapper(main, args)

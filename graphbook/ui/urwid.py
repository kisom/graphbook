# -*- coding: utf-8 -*-

import graphbook.graph as graph
import argparse
import textwrap
import urwid  # type: ignore # urwid doesn't have type annotations

notebook: graph.notebook.Notebook


def build_node_display(node_id):
    node = notebook.noder(node_id)
    body = [urwid.Text("Node: " + node.title), urwid.Divider()]
    for cell in node.cells:
        body.append(urwid.Text(cell.render()))
        body.append(urwid.Text("\n"))
    return urwid.Pile(body)


def display_node(button, node):
    body = build_node_display(node.id)

    done = urwid.Button(u"Ok")
    urwid.connect_signal(done, "click", display)
    main.original_widget = urwid.Filler(
        urwid.Pile([body, urwid.AttrMap(done, None, focus_map="reversed")])
    )


def menu():
    body = [urwid.Text("GraphBook"), urwid.Divider()]
    nodes = notebook.select()
    for node in nodes:
        button = urwid.Button(node.title)
        urwid.connect_signal(button, "click", display_node, node)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def exit_program(button):
    raise urwid.ExitMainLoop()


def keypress_exit(key):
    if key in ["q", "Q", "esc"]:
        raise urwid.ExitMainLoop()


main = None


def display(*args):
    global main
    main = urwid.Padding(menu(), left=2, right=2)
    top = urwid.Overlay(
        main,
        urwid.SolidFill(u"\N{MEDIUM SHADE}"),
        align="center",
        width=("relative", 60),
        valign="middle",
        height=("relative", 60),
        min_width=20,
        min_height=9,
    )
    urwid.MainLoop(
        top, palette=[("reversed", "standout", "")], unhandled_input=keypress_exit
    ).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="graphbook", description="A programmer's knowledge repository"
    )

    # TODO: remove the default when ready
    parser.add_argument(
        "path", help="The path to the GraphBook", default="tests/demobook", nargs="?"
    )
    args = parser.parse_args()
    notebook = graph.notebook.Notebook(args.path)

    display()

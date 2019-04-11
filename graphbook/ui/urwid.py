# -*- coding: utf-8 -*-

from typing import List, Optional
import graphbook.graph as graph
import argparse
import textwrap
import urwid  # type: ignore # urwid doesn't have type annotations


main = None
notebook: Optional[graph.notebook.Notebook] = None
node_stack: List[graph.notebook.NodeEntry] = []
DEFAULT_PATH = "tests/demobook"


def build_node_display(node_id):
    node = notebook.noder(node_id)
    body = [urwid.Text("Node: " + node.title), urwid.Divider()]
    for cell in node.cells:
        body.append(urwid.Text(cell.render()))
        body.append(urwid.Text("\n"))
    if node.links:
        body.append(urwid.Divider())
        body.append(urwid.Text("Linked nodes"))
        for link in node.links:
            lnode = notebook.nodes[link]
            button = urwid.Button(lnode.title)
            urwid.connect_signal(button, "click", jump_nodes, (node, lnode))
            body.append(urwid.AttrMap(button, None, focus_map="reversed"))
        body.append(urwid.Divider())
    return urwid.Pile(body)


def jump_nodes(button, nodeinfo):
    (prev_node, lnode) = nodeinfo
    print(prev_node)
    print(lnode)
    node_stack.append(prev_node)
    display_node(button, lnode)


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
        raise urwid.ExitMainLoop


def setup_notebook(args):
    global notebook

    if not notebook:
        notebook = graph.notebook.Notebook(args.path)


def display(*args):
    global main
    global node_stack

    base_widget = menu()
    if node_stack:
        node = node_stack.pop()
        base_widget = display(node)
    main = urwid.Padding(base_widget, left=2, right=2)
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
        "path", help="The path to the GraphBook", default=DEFAULT_PATH, nargs="?"
    )
    args = parser.parse_args()

    setup_notebook(args)
    display()

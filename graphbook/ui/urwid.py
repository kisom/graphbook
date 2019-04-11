# -*- coding: utf-8 -*-

import graphbook.graph as graph
import argparse
import urwid  # type: ignore # urwid doesn't have type annotations

notebook: graph.notebook.Notebook


def display_node(node):
    response = urwid.Text(
        [node.title, "\n-----\n", notebook.noder(node.id).render(), u"\n"]
    )
    done = urwid.Button(u"Ok")
    urwid.connect_signal(done, "click", exit_program)
    main.original_widget = urwid.Filler(
        urwid.Pile([response, urwid.AttrMap(done, None, focus_map="reversed")])
    )


def menu(title):
    search_box = urwid.Edit("> ")
    body = [urwid.Text(title), search_box, urwid.Divider]
    nodes = notebook.select(search_box.text)
    for node in nodes:
        button = urwid.Button(node.title)
        urwid.connect_signal(button, "click", display_node, node)
        body.append(urwid.AttrMap(button, None, focus_map="reversed"))
    return urwid.ListBox(urwid.SimpleFocusListWalker)


def exit_program(button):
    raise urwid.ExitMainLoop()


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

    main = urwid.Padding(menu("GraphBook"), left=2, right=2)
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
    urwid.MainLoop(top, palette=[("reversed", "standout", "")]).run()

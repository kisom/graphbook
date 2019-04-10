# -*- coding: utf-8 -*-

from flask import Flask, Response
from typing import Any
import json
import os
import sys
from graphbook import graph


def to_json(v: Any, status: int = 200) -> Response:
    return Response(json.dumps(v), status=status, mimetype="application/json")


notebook_dir = os.getcwd()
if len(sys.argv) > 1:
    notebook_dir = sys.argv[1]


app = Flask("graphbook")
notebook = graph.notebook.Notebook(notebook_dir)


@app.route("/")
def index():
    nodes = notebook.select()
    return to_json({"nodes": [node.to_obj() for node in nodes]})


@app.route("/node/<node_id>", methods=["GET", "POST"])
def node_route(node_id):
    node = notebook.noder(node_id)
    if node:
        node = node.to_obj()
    return to_json({"node": node})


if __name__ == "__main__":
    app.run()

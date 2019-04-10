# -*- coding: utf-8 -*-

from flask import Flask
import json
import os
import sys
from graphbook import graph

notebook_dir = os.getcwd()
if len(sys.argv) > 1:
    notebook_dir = sys.argv[1]

app = Flask("graphbook")
notebook = graph.notebook.Notebook(notebook_dir)


@app.route("/")
def index():
    nodes = notebook.select()
    return json.dumps([node.to_obj() for node in nodes])

@app.route("/node/<node_id>", methods=['GET', 'POST'])
def node_route(node_id):
    node = notebook.noder(node_id)
    if node:
        node = node.to_obj()
    return json.dumps({
        'node': node,
    })

    
if __name__ == "__main__":
    app.run()

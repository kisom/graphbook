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
    return json.dumps(nodes)
    


if __name__ == '__main__':
    app.run()

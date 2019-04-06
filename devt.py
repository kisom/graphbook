import pickle
import yaml

import graphbook.graph as graph

node1 = graph.node.Node()
node2 = graph.node.Node()
node1.add(graph.cell.Cell(b'hello, world'))
node1.add(graph.cell.Cell(b'goodbye, world'))
node1.tag('world')
node2.add(graph.cell.Cell(b'''this is an experiment in knowledge management. I'm sure the
s are old hat and whatnot.

l see how it goes.'''))

g = graph.graph.Graph()
g.link(node1, node2)

h = node1.cells[0].dump()
print(h)
print(yaml.dump(h))

print(graph.cell.load_cell(h))

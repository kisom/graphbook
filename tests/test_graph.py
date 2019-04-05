import pickle

from context import graph

def test_serialising():
    node1 = graph.Node()
    node2 = graph.Node()
    node1.add(graph.Cell(b'hello, world'))
    node1.add(graph.Cell(b'goodbye, world'))
    node2.add(graph.Cell(b'''this is an experiment in knowledge management. I'm sure the
ideas are old hat and whatnot.

We'll see how it goes.'''))

    g = graph.Graph()
    g.link(node1, node2)

    gdata = pickle.dumps(g)
    assert(len(gdata) != 0)

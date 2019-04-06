import pickle

from context import graph

def compare_nodes(g1, g2):
    assert(len(g1.nodes) == len(g2.nodes))    
    for node_id in g1.nodes:
        assert(node_id in g2.nodes)
        assert(g1.nodes[node_id] == g2.nodes[node_id])

def test_serialising():
    node1 = graph.Node()
    node2 = graph.Node()
    node1.add(graph.Cell(b'hello, world'))
    node1.add(graph.Cell(b'goodbye, world'))
    node1.tag('world')
    node2.add(graph.Cell(b'''this is an experiment in knowledge management. I'm sure the
ideas are old hat and whatnot.

We'll see how it goes.'''))

    g = graph.Graph()
    g.link(node1, node2)

    gdata = pickle.dumps(g)
    assert(len(gdata) != 0)

    g2 = pickle.loads(gdata)
    assert(g.id == g2.id)
    compare_nodes(g, g2)

    assert(g.tags == g2.tags)

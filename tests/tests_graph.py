import unittest
from pychem.modules import graph


def dijkstra_graph():  # from wikipedia
    g = graph.Graph(directed=False, weighted=True)
    edges = [('1', '2', 7), ('1', '3', 9), ('1', '6', 14), ('2', '3', 10), ('2', '4', 15), ('3', '4', 11),
             ('3', '6', 2), ('4', '5', 6), ('5', '6', 9)]
    g.create_edges(edges)
    return g


def bellman_ford_graph():  # from wikipedia
    g = graph.Graph(directed=True, weighted=True)
    edges = [('t', 'x', 5), ('t', 'y', 8), ('t', 'z', -4), ('x', 't', -2), ('y', 'x', -3), ('y', 'z', 9),
             ('z', 'x', 7), ('z', 's', 2), ('s', 't', 6), ('s', 'y', 7)]
    g.create_edges(edges)
    return g


def ford_fulkerson_graph():  # from homework 5
    g = graph.Graph(directed=True, weighted=True)
    edges = [('s', 'u', 15), ('s', 'v', 5), ('s', 'x', 12), ('u', 'v', 10), ('u', 'x', 8), ('x', 'y', 5),
             ('x', 't', 5), ('t', 'y', 15), ('v', 'z', 8), ('z', 't', 10)]
    g.create_edges(edges)
    return g


def tarjan_graph():  # from wikipedia
    g = graph.Graph(directed=True, weighted=False)
    edges = [('A', 'E'), ('B', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'C'), ('E', 'B'), ('F', 'B'), ('F', 'E'),
             ('F', 'G'), ('G', 'F'), ('G', 'C'), ('H', 'G'), ('H', 'H'), ('H', 'D'), ('B', 'I'), ('I', 'A')]
    g.create_edges(edges)
    return g


def semi_cyclic_graph():
    g = graph.Graph(directed=False, weighted=False)
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('B', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'H'),
             ('H', 'F')]
    g.create_edges(edges)
    return g


class TestGraphAlgorithms(unittest.TestCase):
    def test_graph(self):
        g = graph.Graph()
        self.assertEqual(g.get_edges(), [])
        self.assertEqual(g.get_nodes(), [])
        for node in ['a', 'b', 'c']:
            g.create_node(node)
        for source, sink in [('a', 'b'), ('b', 'c'), ('b', 'd')]:
            g.create_edge(source, sink)
        edges = set()
        for edge in g.get_edges():
            edges.add()
        self.assertEqual(set((g.get_edges())), {('a', 'b'), ('b', 'c'), ('b', 'd')})
        self.assertEqual(set(g.get_nodes()), {'a', 'b', 'c', 'd'})

    def test_dijkstra(self):
        distances, predecessors = graph.dijkstra(dijkstra_graph(), '1')
        self.assertEqual(distances, {'1': 0, '2': 7, '3': 9, '4': 20, '5': 20, '6': 11})
        self.assertEqual(predecessors, {'1': None, '2': '1', '3': '1', '4': '3', '5': '6', '6': '3'})


if __name__ == '__main__':
    unittest.main()

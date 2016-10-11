import unittest
from pychem.modules import graph


def dijkstra_graph():  # from wikipedia
    edges = [('1', '2', 7), ('1', '3', 9), ('1', '6', 14), ('2', '3', 10), ('2', '4', 15), ('3', '4', 11),
             ('3', '6', 2), ('4', '5', 6), ('5', '6', 9)]
    return graph.Graph(edges=edges, directed=False, weighted=True)


def bellman_ford_graph():  # from wikipedia
    edges = [('t', 'x', 5), ('t', 'y', 8), ('t', 'z', -4), ('x', 't', -2), ('y', 'x', -3), ('y', 'z', 9),
             ('z', 'x', 7), ('z', 's', 2), ('s', 't', 6), ('s', 'y', 7)]
    return graph.Graph(edges=edges, directed=True, weighted=True)


def ford_fulkerson_graph():  # from homework 5
    edges = [('s', 'u', 15), ('s', 'v', 5), ('s', 'x', 12), ('u', 'v', 10), ('u', 'x', 8), ('x', 'y', 5),
             ('x', 't', 5), ('t', 'y', 15), ('v', 'z', 8), ('z', 't', 10)]
    return graph.Graph(edges=edges, directed=True, weighted=True)


def tarjan_graph():  # from wikipedia
    edges = [('A', 'E'), ('B', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'C'), ('E', 'B'), ('F', 'B'), ('F', 'E'),
             ('F', 'G'), ('G', 'F'), ('G', 'C'), ('H', 'G'), ('H', 'H'), ('H', 'D'), ('B', 'I'), ('I', 'A')]
    return graph.Graph(edges=edges, directed=True, weighted=False)


def semi_cyclic_graph():
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('B', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'H'),
             ('H', 'F')]
    return graph.Graph(edges=edges, directed=False, weighted=False)


class TestGraphAlgorithms(unittest.TestCase):
    def test_graph(self):
        g = graph.Graph()
        self.assertEqual(g.get_edges(), [])
        self.assertEqual(g.get_nodes(), [])

    def test_dijkstra(self):
        distances, predecessors = graph.dijkstra(dijkstra_graph(), '1')
        self.assertEqual(distances, {'1': 0, '2': 7, '3': 9, '4': 20, '5': 20, '6': 11})
        self.assertEqual(predecessors, {'1': None, '2': '1', '3': '1', '4': '3', '5': '6', '6': '3'})


if __name__ == '__main__':
    unittest.main()

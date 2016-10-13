from queue import Queue


class Node:
    def __init__(self, identifier=None):
        self.identifier = identifier
        self.adj_nodes = set()
        self.edges = set()

    def add_adjacent_node(self, node, edge):
        self.adj_nodes.add(node)
        self.edges.add(edge)


class Edge:
    def __init__(self, source, sink, weight=1):
        self.source = source
        self.sink = sink
        self.weight = weight

    def get_other_node(self, node):
        if self.source == node:
            return self.sink
        if self.sink == node:
            return self.source


class Graph:
    def __init__(self, directed=True, weighted=False):
        self.directed = directed
        self.weighted = weighted

        self.nodes = set()
        self.edges = set()
        self._node_ids = dict()

    def __len__(self):
        return len(self.nodes)

    def yield_edges(self):
        yield from (edge for edge in self.edges)

    def get_edges(self):
        return list(self.yield_edges())

    def yield_nodes(self):
        yield from (node for node in self.nodes)

    def get_nodes(self):
        return list(self.yield_nodes())

    def add_node(self, node):
        if not isinstance(node, Node):
            raise ValueError('"' + str(node) + '" is not an Node.')
        if node not in self.nodes:
            self.nodes.add(node)
            return True
        return False

    def create_node(self, node):
        if node not in self._node_ids:
            nodenode = Node()
            self.nodes.add(nodenode)
            self._node_ids[node] = nodenode
            return True
        return False

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, edge):
        if not isinstance(edge, Edge):
            raise ValueError('"' + str(edge) + '" is not an Edge.')
        self.add_node(edge.source)
        self.add_node(edge.sink)

        self.edges.add(edge)
        edge.source.add_adjacent_node(edge.sink, edge)
        if not self.directed:
            edge.sink.add_adjacent_node(edge.source, edge)

    def create_edge(self, source, sink, weight=None):
        if isinstance(source, Node):
            self.add_node(source)
        else:
            self.create_node(source)
        if isinstance(sink, Node):
            self.add_node(sink)
        else:
            self.create_node(sink)

        if source in self._node_ids:
            source = self._node_ids[source]
        if sink in self._node_ids:
            sink = self._node_ids[sink]

        if not self.weighted:
            weight = 1

        edge = Edge(source, sink, weight)

        self.edges.add(edge)

        source.add_adjacent_node(sink, edge)
        if not self.directed:
            sink.add_adjacent_node(source, edge)

    def create_edges(self, edges):
        for edge in edges:
            source, sink = edge[0], edge[1]
            if self.weighted:
                weight = edge[2]
            else:
                weight = 1
            self.create_edge(source, sink, weight)

    # todo:
    def copy(self, directed=None, weighted=None, nodes=None):
        if directed is None:
            directed = self.directed
        if weighted is None:
            weighted = self.directed
        new_graph = Graph(directed=directed, weighted=weighted)
        for node in self.yield_nodes():
            if nodes is None or node in nodes:
                new_graph.add_node(node)
        for edge in self.yield_edges():
            if nodes is None or (edge.source in nodes and edge.sink in nodes):
                new_graph.create_edge(edge.source, edge.sink, edge.weight)
        return new_graph


############################################################
#                  Dijkstra's algorithm                    #
############################################################


def dijkstra(graph, source, sink=None, _allow_direct_edge=True):
    """
    Dijkstra's algorithm for finding the shortest paths in a weighted graph starting with node 'source'.
    If the graph contains negative edges, it is better to use the Bellman-Ford algorithm.
    Worst case performance: O(V²)

    If a node 'sink' is specified, the algorithm terminates if the weight of the shortest path to that
    node is known. This is useful if you only need to know the path to that node.

    '_allow_direct_edge' is a parameter useful for the algorithm that finds non-reducible cycles.
    """
    unvisited_nodes = set()
    distance = dict()
    predecessor = dict()
    for node in graph.yield_nodes():
        distance[node] = float('inf')
        predecessor[node] = None
        unvisited_nodes.add(node)
    distance[source] = 0

    while unvisited_nodes:
        closest_node = None
        lowest_distance = float('inf')
        for node in unvisited_nodes:
            if distance[node] < lowest_distance:
                lowest_distance = distance[node]
                closest_node = node
        current_node = closest_node
        if current_node is None:
            break
        unvisited_nodes.remove(current_node)

        # if the sink node is picked from unvisited_nodes it is certain its lowest weight path is known
        if current_node == sink:
            break

        for edge in current_node.edges:
            adj_node = edge.get_other_node(current_node)
            if current_node == source and adj_node == sink and not _allow_direct_edge:
                continue
            new_dist = distance[current_node] + edge.weight
            if new_dist < distance[adj_node]:
                distance[adj_node] = new_dist
                predecessor[adj_node] = current_node

    return distance, predecessor


############################################################
#                 Bellman-Ford algorithm                   #
############################################################


def bellman_ford(graph, source, sink=None, _allow_direct_edge=True):
    """
    The Bellman-Ford algorithm for finding the shortest paths in a weighted graph starting with node 'source'.
    This algorithm can be used with graphs with negative weighted edges, as long as the graph does not contain
    negative cycles. If negative cycles are encountered the algorithm raises a ValueError.
    Worst case performance: O(V*E)

    This algorithm can't be sped up by specifying a sink node. It is still included for consistency between
    the shortest path algorithms.

    '_allow_direct_edge' is a parameter useful for the algorithm that finds non-reducible cycles.
    """
    distance = dict()
    predecessor = dict()
    edges = list()
    for edge in graph.edges:
        if (edge.source == source and edge.sink == sink) or (edge.sink == source and edge.source == sink) \
                and not _allow_direct_edge:
            continue
        edges.append(edge)
    for node in graph.yield_nodes():
        distance[node] = None
        predecessor[node] = None
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for edge in edges:
            if distance[edge.source] is not None:
                if distance[edge.sink] is None or distance[edge.source] + edge.weight < distance[edge.sink]:
                    distance[edge.sink] = distance[edge.source] + edge.weight
                    predecessor[edge.sink] = edge.source
            if not graph.directed:
                if distance[edge.sink] is not None:
                    if distance[edge.source] is None or distance[edge.sink] + edge.weight < distance[edge.source]:
                        distance[edge.source] = distance[edge.sink] + edge.weight
                        predecessor[edge.source] = edge.sink

    for edge in edges:
        if distance[edge.source] and distance[edge.source] + edge.weight < distance[edge.sink]:
            raise ValueError('Graph contains negative cycles!')
        if not graph.directed:
            if distance[edge.sink] and distance[edge.sink] + edge.weight < distance[edge.source]:
                raise ValueError('Graph contains negative cycles!')

    return distance, predecessor


############################################################
#                          BFS                             #
############################################################


def bfs_shortest_paths(graph, source, sink=None, _allow_direct_edge=True):
    """
    Breadth-first search for finding the shortest paths in an unweighted or weighted graph starting with
    node 'source'. This algorithm finds the paths with the least amount of edges to the other nodes. It does
    not take edge weight into account and is more efficient than Dijkstra and Bellman-Ford.
    Worst case performance: O(V)

    If a node 'sink' is specified, the algorithm terminates if the weight of the shortest path to that
    node is known. This is useful if you only need to know the path to that node.

    '_allow_direct_edge' is a parameter useful for the algorithm that finds non-reducible cycles.
    """
    visited_nodes = {source}
    predecessor = dict()
    distance = {source: 0}
    bfs_queue = Queue()
    bfs_queue.put(source)
    while not bfs_queue.empty():
        current_node = bfs_queue.get()
        for adj_node in graph.adj_nodes(current_node):
            if adj_node == sink and current_node == source and not _allow_direct_edge:
                continue
            if adj_node not in visited_nodes:
                predecessor[adj_node] = current_node
                distance[adj_node] = distance[current_node] + 1
                visited_nodes.add(adj_node)
                bfs_queue.put(adj_node)
            if adj_node == sink:
                if _allow_direct_edge or current_node != source:
                    break
    return distance, predecessor


############################################################
#            generalizing path find algorithm              #
############################################################


def find_shortest_path(graph, source, sink, alg='bellmanford', _allow_direct_edge=True):
    """
    'alg' is the parameter that determines what path-finding algorithm is used. Valid options are; 'dijkstra',
    'bellmanford', and 'bfs'. Note: bfs does not take edge weight into account but finds the path with the
    lowest amount of edges.

    '_allow_direct_edge' determines if an edge from node_from to node_to also counts as valid path. This option
    is essential for finding non reducible cycles.

    returns a list of nodes starting with node_from, ending with node_to.
    """
    algorithm = _choose_path_find_algorithm(alg)
    _, predecessors = algorithm(graph, source, sink=sink, _allow_direct_edge=_allow_direct_edge)
    node = sink
    path = [node]
    while node != source:
        if node not in predecessors:
            return []
        node = predecessors[node]
        path.append(node)
    path.reverse()
    return path


def _choose_path_find_algorithm(string):
    string = string.lower()
    if string in ['dijkstra']:
        algorithm = dijkstra
    elif string in ['bellmanford', 'bellman', 'ford']:
        algorithm = bellman_ford
    elif string in ['bfs', 'breadthfirstsearch']:
        algorithm = bfs_shortest_paths
    else:
        raise ValueError('"' + string + '" is not recognized as a path finding algorithm. Valid options are:\n'
                                        ' - dijkstra\n'
                                        ' - bellmanford\n'
                                        ' - bfs')
    return algorithm


############################################################
#                Ford-Fulkerson algorithm                  #
############################################################


def ford_fulkerson(graph, source, sink, force_unweighted=False):
    """
    The Ford-Fulkerson algorithm finds the maximum flow between the source node and the sink node in a
    flow network graph. It also finds the 'minimum cut', a list of nodes that are the bottleneck for the
    maximum flow.

    If 'force_unweighted' is true, all edges have flow rate one.
    """
    flow = dict()
    capacity = dict()
    backwards_edges = set()
    for node in graph:
        for adj_node, edge_weight in graph[node]:
            if not graph.weighted or force_unweighted:
                edge_weight = 1
            capacity[(node, adj_node)] = edge_weight
            flow[(node, adj_node)] = 0
            flow[(adj_node, node)] = 0
            backwards_edges.add((adj_node, node))

    path = _find_ford_fulkerson_path(graph, source, sink, flow, [], force_unweighted)
    while path is not None:
        residuals = [capacity[edge] - flow[edge] for edge in path]
        min_flow = min(residuals)
        for node_from, node_to in path:
            flow[(node_from, node_to)] += min_flow
            flow[(node_to, node_from)] -= min_flow
        path = _find_ford_fulkerson_path(graph, source, sink, flow, [])

    min_cut = [edge for edge, flow_rate in flow.items() if edge in capacity and capacity[edge] == flow_rate]
    max_flow = sum(flow[(source, adj_node)] for adj_node, _ in graph[source])
    return max_flow, min_cut


def _find_ford_fulkerson_path(graph, source, sink, flow, path, force_unweighted=False):
    if source == sink:
        return path
    for adj_node, edge_weight in graph[source]:
        if not graph.weighted or force_unweighted:
            edge_weight = 1
        residual = edge_weight - flow[(source, adj_node)]
        if residual > 0 and (source, adj_node) not in path:
            result = _find_ford_fulkerson_path(graph, adj_node, sink, flow, path + [(source, adj_node)])
            if result is not None:
                return result


############################################################
#                  Get all degree-1 nodes                  #
############################################################


def yield_end_nodes(graph):
    if graph.directed:
        raise ValueError('Graph should be undirected.')
    for node in graph:
        edges = graph[node]
        if len(edges) == 1:
            yield node


def list_end_nodes(graph):
    return list(yield_end_nodes(graph))


############################################################
#               Get the degree of every node               #
############################################################


def get_node_degrees(graph):
    if graph.directed:
        return _get_node_degrees_directed(graph)
    else:
        return _get_node_degrees_undirected(graph)


def _get_node_degrees_undirected(graph):
    degrees = dict()
    for node in graph:
        edges = graph[node]
        degrees[node] = len(edges)
    return degrees


def _get_node_degrees_directed(graph):
    out_degrees = dict()
    in_degrees = dict()
    if graph.directed:
        for node in graph:
            in_degrees[node] = 0
    for node in graph:
        edges = graph[node]
        out_degrees[node] = len(edges)
        for other_node, _ in graph:
            in_degrees[other_node] += 1
    in_out_degrees = dict()
    for node in out_degrees:
        in_out_degrees[node] = (out_degrees[node], in_degrees[node])
    return in_out_degrees


############################################################
# Compressing the graph to only junction and ending nodes. #
############################################################


def get_all_degree2_chains(graph):
    """
    Works unless the graph is a cycle containing only degree-2 nodes. Also does not work if graph is a chain with
    self edging nodes at both ends.
    :param graph: The graph containing all the nodes and edges.
    :return: list containing lists of chained nodes. First and last elements are not-degree-2 nodes
    """
    if graph.directed:
        raise ValueError('Graph should be undirected.')

    node_degrees = get_node_degrees(graph)
    marked_nodes = set()
    chains = list()

    for node in graph:
        if node in marked_nodes:
            continue

        adj_nodes = [node for node, _ in graph[node]]
        is_intersection_node = False
        if node_degrees[node] != 2:
            is_intersection_node = True

        if is_intersection_node:
            for adj_node in adj_nodes:
                if adj_node not in marked_nodes and node_degrees[adj_node] == 2:
                    new_chain = _build_degree2_chain(graph, adj_node, [node])
                    for chain_node in new_chain[1:-1]:
                        marked_nodes.add(chain_node)
                    chains.append(new_chain)
    return chains


def _build_degree2_chain(graph, node, chain):
    """
    :param graph: The graph containing all the nodes and edges.
    :param node: A 2-degree node which becomes the second element in the chain.
    :param chain: This is a bit weird, but chain must be a non-degree2 node adjacent to node.
    :return: list starting and ending with a non-degree-2 node and all degree-2 node in between.
    """
    chain.append(node)
    if len(graph[node]) != 2:
        return chain
    for other_node, _ in graph[node]:
        if other_node == node:
            return chain
        if other_node not in chain:
            return _build_degree2_chain(graph, other_node, chain)


def _merge_degree2_nodes(graph):
    new_graph = Graph()
    chains = get_all_degree2_chains(graph)
    # todo


def _demerge_degree2_nodes(graph):
    pass


def _remove_degree1_nodes(graph, recursive=True):
    pass


def chordless_cycles(graph):
    for node_from in graph:
        for node_to, _ in graph[node_from]:
            candidated = list()


############################################################
#                 Tarjan's SCC algorithm                   #
############################################################


def tarjan(graph):
    """
    Tarjan's strongly connected components algorithm. The algorithm finds all SCCs in a graph.

    A list of SCC sets is returned
    """
    i = [0]
    stack = list()
    onstack = set()
    index = dict()
    lowlink = dict()

    scc_list = list()
    for node in graph:
        if node not in index:
            for scc in _tarjan_strongconnect(graph, node, i, stack, onstack, index, lowlink):
                scc_list.append(scc)
    return scc_list


def _tarjan_strongconnect(graph, node, i, stack, onstack, index, lowlink):
    index[node] = i[0]
    lowlink[node] = i[0]
    i[0] += 1
    stack.append(node)
    onstack.add(node)

    for adj_node, _ in graph[node]:
        if adj_node not in index:
            yield from _tarjan_strongconnect(graph, adj_node, i, stack, onstack, index, lowlink)
        elif adj_node in onstack:
            lowlink[node] = min(lowlink[node], lowlink[adj_node])

    if lowlink[node] == index[node]:
        scc = set()
        other_node = stack.pop()
        onstack.remove(other_node)
        scc.add(other_node)
        while other_node != node:
            other_node = stack.pop()
            onstack.remove(other_node)
            scc.add(other_node)
        yield scc


############################################################
#                  David's nrc algorithm                   #
############################################################


def get_cyclic_nodes(graph):
    cyclic_nodes = set()
    for node in graph:
        if node in cyclic_nodes:
            continue
        for adj_node in graph.adj_nodes(node):
            path = find_shortest_path(graph, adj_node, node, alg='bfs', _allow_direct_edge=graph.directed)
            for path_node in path:
                cyclic_nodes.add(path_node)
    return cyclic_nodes


def get_non_reducible_cycles(graph, alg='bellmanford'):
    if not graph.weighted:
        alg = 'bfs'

    nrc_lists = list()
    nrc_sets = list()
    for node_from, node_to, *_ in graph.yield_edges():
        nrc_nodes = find_shortest_path(graph, node_to, node_from, alg=alg, _allow_direct_edge=False)
        if nrc_nodes:
            nrc_set = set(nrc_nodes)
            if nrc_set not in nrc_sets:
                nrc_sets.append(nrc_set)
                nrc_lists.append(nrc_nodes)
    return nrc_lists


############################################################
#                                                          #
############################################################


if __name__ == '__main__':
    e = [('a', 'b'), ('b', 'c'), ('c', 'a'), ('c', 'd'), ('d', 'e'), ('e', 'f'), ('f', 'g'), ('g', 'h'), ('h', 'f'),
         ('e', 'i')]
    g = Graph(edges=e, directed=False, weighted=False)
    e = [('1', '2', 7), ('1', '3', 9), ('1', '6', 14), ('2', '3', 10), ('2', '4', 15), ('3', '4', 11),
         ('3', '6', 2), ('4', '5', 6), ('5', '6', 9)]
    g2 = Graph(edges=e, directed=False, weighted=True)
    e = [('t', 'x', 5), ('t', 'y', 8), ('t', 'z', -4), ('x', 't', -2), ('y', 'x', -3), ('y', 'z', 9),
         ('z', 'x', 7), ('z', 's', 2), ('s', 't', 6), ('s', 'y', 7)]
    g3 = Graph(edges=e, directed=True, weighted=True)
    nrcs = get_non_reducible_cycles(g3, alg='dijkstra')
    for nrc in nrcs:
        print(nrc)

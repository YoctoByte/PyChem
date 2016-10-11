from queue import Queue


class Graph:
    def __init__(self, nodes=None, edges=None, directed=True, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self._nodes = dict()
        self.edges = set()

        self.add_nodes(nodes)
        self.add_edges(edges)

    def __iter__(self):
        for node in self._nodes:
            yield node

    def __getitem__(self, node):
        return self._nodes[node]

    def __len__(self):
        return len(self._nodes)

    def yield_edges(self):
        edges = set()
        for node_from in self:
            for node_to, edge_weight in self[node_from]:
                if not self.directed:
                    if (node_to, node_from, edge_weight) in edges:
                        continue
                    edges.add((node_from, node_to, edge_weight))
                if self.weighted:
                    yield (node_from, node_to, edge_weight)
                else:
                    yield (node_from, node_to)

    def get_edges(self):
        return list(self.yield_edges())

    def yield_nodes(self):
        for node in self:
            yield node

    def get_nodes(self):
        return list(self)

    def adj_edges(self, node):
        adj_edges = list()
        for adj_node, edge_weight in self[node]:
            if self.weighted:
                adj_edges.append((node, adj_node, edge_weight))
            else:
                adj_edges.append((node, adj_node))
        return adj_edges

    def adj_nodes(self, node):
        adj_nodes = list()
        for adj_node, _ in self[node]:
            adj_nodes.append(adj_node)
        return adj_nodes

    def add_node(self, node):
        if node not in self:
            self._nodes[node] = set()

    def add_nodes(self, nodes):
        if not nodes:
            return
        for node in nodes:
            self.add_node(node)

    def add_edge(self, node_from, node_to, edge_weight=None):
        if node_from not in self:
            self._nodes[node_from] = set()
        if node_to not in self:
            self._nodes[node_to] = set()
        if not self.weighted:
            edge_weight = 1
        self._nodes[node_from].add((node_to, edge_weight))
        if not self.directed:
            self._nodes[node_to].add((node_from, edge_weight))
        self.edges.add((node_from, node_to, edge_weight))
        if not self.directed:
            self.edges.add((node_to, node_from, edge_weight))

    def add_edges(self, edges):
        if not edges:
            return
        for edge in edges:
            node_from, node_to = edge[0], edge[1]
            if self.weighted:
                edge_weight = edge[2]
            else:
                edge_weight = 1
            self.add_edge(node_from, node_to, edge_weight)

    def copy(self, directed=None, weighted=None, nodes=None):
        if directed is None:
            directed = self.directed
        if weighted is None:
            weighted = self.directed
        new_graph = Graph(directed=directed, weighted=weighted)
        for node in self:
            if nodes and node in nodes:
                new_graph.add_node(node)
        for node_from, node_to, edge_weight in self.edges:
            if nodes and node_from in nodes and node_to in nodes:
                new_graph.add_edge(node_from, node_to, edge_weight)
        return new_graph

    def deepcopy(self, directed=None, weighted=None, nodes=None):
        if directed is None:
            directed = self.directed
        if weighted is None:
            weighted = self.directed
        new_graph = Graph(directed=directed, weighted=weighted)
        new_node = dict()
        for node in self:
            if nodes and node in nodes:
                try:
                    new_node[node] = node.copy()
                except AttributeError:
                    new_node[node] = node
                new_graph.add_node(new_node[node])
        for node_from, node_to, edge_weight in self.edges:
            if nodes and node_from in nodes and node_to in nodes:
                try:
                    edge_weight = edge_weight.copy()
                except AttributeError:
                    pass
                new_graph.add_edge(new_node[node_from], new_node[node_to], edge_weight)
        return new_graph


############################################################
#                  Dijkstra's algorithm                    #
############################################################


def dijkstra(graph, source, sink=None, _allow_direct_edge=True):
    unvisited_nodes = set()
    distance = dict()
    predecessor = dict()
    for node in graph:
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

        if current_node == sink:
            break

        for adj_node, edge_weight in graph[current_node]:
            if current_node == source and adj_node == sink and not _allow_direct_edge:
                continue
            if not graph.weighted:
                edge_weight = 1
            new_dist = distance[current_node] + edge_weight
            if new_dist < distance[adj_node]:
                distance[adj_node] = new_dist
                predecessor[adj_node] = current_node

    return distance, predecessor


def dijkstra_get_path(graph, source, sink, _allow_direct_edge=True):
    _, predecessors = dijkstra(graph, source, sink=sink, _allow_direct_edge=_allow_direct_edge)
    node = sink
    path = [node]
    while node != source:
        if node not in predecessors:
            return []
        node = predecessors[node]
        path.append(node)
    path.reverse()
    return path


############################################################
#                 Bellman-Ford algorithm                   #
############################################################


def bellman_ford(graph, source):
    distance = dict()
    predecessor = dict()
    edges = list()
    for node in graph:
        distance[node] = None
        predecessor[node] = None
        for adj_node, edge_weight in graph[node]:
            if not graph.weighted:
                edge_weight = 1
            edges.append((node, adj_node, edge_weight))
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for node_from, node_to, edge_weight in edges:
            if distance[node_from] is not None:
                if distance[node_to] is None or distance[node_from] + edge_weight < distance[node_to]:
                    distance[node_to] = distance[node_from] + edge_weight
                    predecessor[node_to] = node_from

    for node_from, node_to, edge_weight in edges:
        if distance[node_from] + edge_weight < distance[node_to]:
            raise ValueError('Graph contains negative cycles!')

    return distance, predecessor


def bellman_ford_get_path(graph, source, sink, _allow_direct_edge=True):
    _, predecessors = dijkstra(graph, source, sink=sink, _allow_direct_edge=_allow_direct_edge)
    node = sink
    path = [node]
    while node != source:
        if node not in predecessors:
            return []
        node = predecessors[node]
        path.append(node)
    path.reverse()
    return path


############################################################
#                          BFS                             #
############################################################


def bfs_shortest_paths(graph, source, sink=None, _allow_direct_edge=True):
    pass


def bfs_get_path(graph, source, sink, _allow_direct_edge=True):
    """
    O(V) time efficiency
    :param graph:
    :param source:
    :param sink:
    :param _allow_direct_edge: This parameter determines if an edge from node_from to node_to also counts as valid path.
    :return: return a list of nodes starting with node_from, ending with node_to.
    """
    visited_nodes = {source}
    predecessor = dict()
    bfs_queue = Queue()
    bfs_queue.put(source)
    while not bfs_queue.empty():
        current_node = bfs_queue.get()
        for adj_node in graph.adj_nodes(current_node):
            if adj_node == sink and current_node == source and not _allow_direct_edge:
                continue
            if adj_node not in visited_nodes:
                predecessor[adj_node] = current_node
                visited_nodes.add(adj_node)
                bfs_queue.put(adj_node)
            if adj_node == sink:
                if _allow_direct_edge or current_node != source:
                    path = list()
                    path_node = sink
                    while path_node != source:
                        path.append(path_node)
                        path_node = predecessor[path_node]
                    path.append(source)
                    return list(reversed(path))
    return []


############################################################
#            generalizing path find algorithm              #
############################################################


def _choose_path_find_algorithm(string):
    string = string.lower().replace('-', '').replace('_', '').replace(' ', '')
    if string in ['dijkstra']:
        algorithm = dijkstra_get_path
    elif string in ['bellmanford', 'bellman', 'ford']:
        algorithm = bellman_ford_get_path
    elif string in ['bfs', 'breadthfirstsearch']:
        algorithm = bfs_get_path
    else:
        raise ValueError('"' + string + '" is not recognized as a path finding algorithm. Valid options are:\n'
                                        ' - dijkstra\n'
                                        ' - bellmanford\n'
                                        ' - bfs')
    return algorithm


############################################################
#                Ford-Fulkerson algorithm                  #
############################################################


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


def ford_fulkerson(graph, source, sink, force_unweighted=False):
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


############################################################
#                  Get all degree-1 nodes                  #
############################################################


def yield_end_nodes(graph):
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
#                                                          #
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
            path = bfs_get_path(graph, adj_node, node, _allow_direct_edge=graph.directed)
            for path_node in path:
                cyclic_nodes.add(path_node)
    return cyclic_nodes


def get_non_reducible_cycles(graph, force_unweighted=False, alg='dijkstra'):

    nrc_lists = list()
    nrc_sets = list()
    for node_from, node_to, *_ in graph.yield_edges():
        if graph.weighted and not force_unweighted:
            nrc_nodes = dijkstra_get_path(graph, node_to, node_from, _allow_direct_edge=False)
        else:
            nrc_nodes = bfs_get_path(graph, node_to, node_from, _allow_direct_edge=False)
            print(nrc_nodes)
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
    nrcs = get_non_reducible_cycles(g3)
    for nrc in nrcs:
        print(nrc)

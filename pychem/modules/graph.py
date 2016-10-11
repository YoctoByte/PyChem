from queue import Queue


class Graph:
    def __init__(self, nodes=None, edges=None, edge_ids=None, directed=True, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self._nodes = dict()
        self.edges = set()

        # todo
        if edge_ids:
            pass

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

    # todo: directed, weighted
    def copy(self, directed=None, weighted=None):
        new_graph = Graph()
        new_node = dict()
        for node in self:
            try:
                new_node[node] = node.copy()
            except AttributeError:
                new_node[node] = node
            new_graph.add_node(new_node[node])
        for node_from, node_to, edge_weight in self.edges:
            try:
                edge_weight = edge_weight.copy()
            except AttributeError:
                pass
            new_graph.add_edge(new_node[node_from], new_node[node_to], edge_weight)
        return new_graph


############################################################
#                  Dijkstra's algorithm                    #
############################################################


def dijkstra(graph, source, sink=None, force_unweighted=False):
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
        unvisited_nodes.remove(current_node)

        if current_node == sink:
            break

        for adj_node, edge_weight in graph[current_node]:
            if not graph.weighted or force_unweighted:
                edge_weight = 1
            new_dist = distance[current_node] + edge_weight
            if new_dist < distance[adj_node]:
                distance[adj_node] = new_dist
                predecessor[adj_node] = current_node

    return distance, predecessor


############################################################
#                 Bellman-Ford algorithm                   #
############################################################


def bellman_ford(graph, source, force_unweighted=False):
    distance = dict()
    predecessor = dict()
    edges = list()
    for node in graph:
        distance[node] = None
        predecessor[node] = None
        for adj_node, edge_weight in graph[node]:
            if not graph.weighted or force_unweighted:
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
#                    David's algorithm                     #
############################################################


def is_reachable(graph, node_from, node_to):
    """
    O(V)
    :param graph:
    :param node_from:
    :param node_to:
    :return: True if there is a path from node_from to node_to. Otherwise return False
    """
    visited_nodes = {node_from}
    bfs_queue = Queue()
    bfs_queue.put(node_from)
    while bfs_queue:
        current_node = bfs_queue.get()
        for adj_node in graph.adj_nodes(current_node):
            if adj_node == node_to:
                return True
            if adj_node not in visited_nodes:
                visited_nodes.add(adj_node)
                bfs_queue.put(adj_node)
    return False


# todo: not returning the right nodes
def get_cyclic_nodes(graph):
    cyclic_nodes = set()
    for node in graph:
        mark = dict()
        border = set()
        for adj_node in graph.adj_nodes(node):
            mark[adj_node] = adj_node
            border.add(adj_node)

        is_cyclic = False
        while border:
            border_node = border.pop()
            for adj_node in graph.adj_nodes(border_node):
                if adj_node in mark:
                    if not mark[adj_node] == mark[border_node]:
                        is_cyclic = True
                        break
                else:
                    mark[adj_node] = mark[border_node]
                    if adj_node != node:
                        border.add(adj_node)
            if is_cyclic:
                break
        if is_cyclic:
            cyclic_nodes.add(node)
    return cyclic_nodes


def non_reducible_cycles(graph):
    cyclic_nodes = get_cyclic_nodes(graph)


############################################################
#                                                          #
############################################################

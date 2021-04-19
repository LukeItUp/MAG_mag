import random
import networkx as nx


def read_file(file_path):
    graph = nx.read_pajek(file_path)
    graph = nx.DiGraph(graph)
    return graph


def prepare_random_weights(graph, max_w_val=1):
    weights = dict()
    for edge in graph.edges:
        if max_w_val == 1:
            weights[edge] = random.random()
        else:
            weights[edge] = random.randint(0, max_w_val)
    return weights


def prepare_fixed_weights(graph, p=0.5):
    weights = dict()
    for edge in graph.edges:
        weights[edge] = p
    return weights


def f_pow_x_alpha(weights, alpha=2):
    for key in weights.keys():
        weights[key] = weights[key] ** 2
    return weights


def intermediate_subgraph(graph, source, target):
    paths = nx.all_simple_paths(graph, source, target)
    nodes = set()
    for path in paths:
        for node in path:
            nodes.add(node)
    return nx.induced_subgraph(graph, nodes)


def component(graph, nodes, root, reverse=False):
    component = dict()
    for node in graph:
        component[node] = False

    if root in nodes:
        component[root] = True
        stack = [root]
        while len(stack) > 0:
            node = stack.pop(0)
            edges = graph.in_edges(node) if reverse else graph.out_edges(node)
            for edge in edges:
                neighbor = edge[0] if reverse else edge[1]
                if neighbor in nodes and not component[neighbor]:
                    component[neighbor] = True
                    stack.append(neighbor)

    return component


def monte_carlo(graph, probabilites, source, target, samples=100000):
    def get_sample():
        stack = [source]
        seen = dict()
        for node in graph:
            seen[node] = True if node is source else False

        while len(stack) > 0:
            node = stack.pop(0)
            for edge in graph.out_edges(node):
                succ = edge[1]
                if random.random() < probabilites[edge] and not seen[succ]:
                    seen[succ] = True
                    stack.append(succ)
        #return nx.induced_subgraph(graph, [k for (k, v) in seen.items() if v])
        return component(graph, [k for (k, v) in seen.items() if v], target, reverse=True)

    intermediacies = dict()
    for node in graph:
        intermediacies[node] = 0

    for _ in range(samples):
        sample = get_sample()
        for (k,v) in sample.items():
            if v:
                intermediacies[k] += 1

    for (k, v) in intermediacies.items():
        intermediacies[k] = v/samples

    return intermediacies


graph_path = 'data/clanek.net'
source = "1"
target = "12"
graph = None
weights = dict()


if __name__ == '__main__':
    graph = read_file(graph_path)
    intermediate_graph = intermediate_subgraph(graph, source, target)
    weights = prepare_fixed_weights(intermediate_graph)
    intermediacies = monte_carlo(graph, weights, source, target)
    print("Intermediacies")
    for i in sorted([i for i in intermediacies.items()], key=lambda x: x[1], reverse=True):
        if i[0] == source:
            print("source", i[1])
        elif i[0] == target:
            print("target", i[1])
        else:
            print(i)

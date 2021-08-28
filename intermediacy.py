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

    print(f'0/{samples}', end='')
    for i in range(samples):
        sample = get_sample()
        for (k,v) in sample.items():
            if v:
                intermediacies[k] += 1
        print(f'\r{i}/{samples} samples done', end='')
    print(f'\r{i+1}/{samples} samples done')
    for (k, v) in intermediacies.items():
        intermediacies[k] = v/samples

    return intermediacies


def f_pow_x_alpha(weights, alpha=2.0):
    print(f'p function: f(x) = x^alpha | alpha: {alpha}')
    for key in weights.keys():
        print('.', end='')
        weights[key] = weights[key] ** alpha
    return weights


def f_pow_alpha_x(weights, alpha=2.0):
    print(f'p function: f(x) = alpha^x | alpha: {alpha}')
    for key in weights.keys():
        weights[key] = alpha ** weights[key]
    return weights


def f_mo(weights, alpha=None):
    if alpha is None:
        print('alpha is average weight')
        alpha = sum([i for i in weights.values()]) / len(weights)
    print(f'p function: f(x) = x / (x + alpha) | alpha: {alpha}')
    for key in weights.keys():
        weights[key] = weights[key]/(weights[key] + alpha)
    return weights

import sys


if __name__ == '__main__':
    graph = nx.read_pajek('./data/arxiv_network.net')
    source = "21409"
    for node in ["40398", "158497", "100709", "78375", "78374", "85961", "78377", "86231", "86230", "59586", "69933", "59584", "59359", "59585", "59358", "40399", "65527", "89463", "89462", "72494", "51680", "51679", "38840", "114456", "101912", "94863", "92193", "85149", "92202", "80641", "77194", "83452", "73639", "66044", "61359", "94865", "94864", "80782", "78793", "91842", "105380", "91843", "76011", "74656", "73636", "60018", "82517", "81852", "60593", "96034", "96033", "57271", "56428", "94927", "86165", "53943", "51101", "47071", "5077", "94012", "56427", "41057", "124571", "71548", "37039", "56821", "77832", "87404", "112307", "107549", "55191", "47033", "47021", "59353", "53723", "57410", "47474", "47066", "46529", "39315", "79069", "51270", "46530", "37461", "37038", "35082", "5074"]:
        g = intermediate_subgraph(graph, source, node)
        print(node, 'len:', len(g))
        sys.stdout.flush()

sys.exit()

graph_path = 'data/clanek.net'
source = "1"
target = "12"
n_samples = 10000000
alpha = 0.0000001
random_weights = True
w_max = 1000

graph = None
weights = dict()

if __name__ == '__main__':
    print('---------------------------------------')
    print(f'network: {graph_path}')
    print(f'source: {source} | target: {target} | max w value: {w_max}')

    graph = read_file(graph_path)
    intermediate_graph = intermediate_subgraph(graph, source, target)
    if random_weights:
        weights = prepare_random_weights(graph, max_w_val=w_max)
    else:
        weights = prepare_fixed_weights(graph, p=w_max)

    # --------------------- Weight to probability functions ---------------------
    #probabilities = f_pow_x_alpha(weights, alpha=alpha)
    probabilities = f_pow_alpha_x(weights, alpha=alpha)
    #probabilities = f_mo(weights, alpha=alpha)
    # ---------------------------------------------------------------------------

    intermediacies = monte_carlo(graph, probabilities, source, target, samples=n_samples)
    print("\nIntermediacies")
    for i in sorted([i for i in intermediacies.items()], key=lambda x: x[1], reverse=True):
        if i[0] == source:
            print("source", i[1])
        elif i[0] == target:
            print("target", i[1])
        else:
            print(i)

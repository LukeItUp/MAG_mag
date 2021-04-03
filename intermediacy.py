import random
import networkx as nx

graph_path = 'data/clanek.net'
graph = None
weights = dict()


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
        weights[key] = weights[key]**2
    return weights


def calculate_intermediacy(graph, edge_p, source, target):
    intermediacy = dict()
    # preparing for s_v and v_t intermediacies
    for node in graph:
        if node == source or node == target:
            intermediacy[node] = [1, 1]
        else:
            intermediacy[node] = [None, None]

    # calculating in probabilites
    stack = [source]
    while stack:
        node = stack.pop(0)
        if node is source:
            stack.extend(graph.neighbors(node))
            continue
        if node is target:
            continue

        tmp = 0
        break_flag = False
        in_edges = [i for i in graph.in_edges(node)]
        for in_edge in in_edges:
            try:
                tmp += intermediacy[in_edge[0]][0] * edge_p[in_edge]
            except:
                stack.append(node)
                break_flag = True
                break
        if break_flag:
            continue
        else:
            intermediacy[node][0] = tmp

        for n in graph.neighbors(node):
            if n not in stack:
                stack.append(n)

    # calculating out probabilities
    stack = [target]
    while stack:
        node = stack.pop(0)
        if node is target:
            for e in graph.in_edges(node):
                stack.append(e[0])
            continue
        if node is source:
            continue

        tmp = 0
        break_flag = False
        out_edges = [i for i in graph.out_edges(node)]
        for out_edge in out_edges:
            try:
                tmp += intermediacy[out_edge[1]][1] * edge_p[out_edge]
            except:
                stack.append(node)
                break_flag = True
                break
        if break_flag:
            continue
        else:
            intermediacy[node][1] = tmp

        for e in graph.in_edges(node):
            if e[0] not in stack:
                stack.append(e[0])

    for item in intermediacy.items():
        intermediacy[item[0]] = item[1][0] * item[1][1]

    return intermediacy


if __name__ == '__main__':
    graph = read_file(graph_path)
    #weights = prepare_random_weights(graph, max_w_val=1)
    weights = prepare_fixed_weights(graph)
    print("Weights", [i for i in weights.items()])

    #probabilities = f_pow_x_alpha(weights)
    probabilities = weights
    print("Probabilities:", [i for i in probabilities.items()])

    intermediacies = calculate_intermediacy(graph, probabilities, "1", "12")
    print("Intermediacies", [i for i in intermediacies.items()])

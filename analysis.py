import networkx as nx

def walk(graph, node, search, found):
    if len(search) == 0:
        return found
    if node in search:
        search.remove(node)
        found.append(node)
        return found
    for n, _ in graph.in_edges(node):
        walk(graph, n, search, found)


output = []
def walk2(graph, node):
    for n, _ in graph.in_edges(node):
        output.append(graph.nodes[n]["title"])
        walk2(graph, n)


def stack_walk_reverse(graph, node):
    stack = [node]
    node_titles = []
    for node in graph:
        graph.nodes[node]['seen'] = False

    while len(stack) > 0:
        node = stack.pop(0)
        if graph.nodes[node]['seen']:
            continue
        graph.nodes[node]['seen'] = True
        #print(graph.nodes[node]['title'])
        node_titles.append(node)
        for node, _ in graph.in_edges(node):
            stack.append(node)
    return node_titles


def stack_walk(graph, node):
    stack = [node]
    node_titles = []
    for node in graph:
        graph.nodes[node]['seen'] = False

    while len(stack) > 0:
        node = stack.pop(0)
        if graph.nodes[node]['seen']:
            continue
        graph.nodes[node]['seen'] = True
        #print(graph.nodes[node]['title'])
        node_titles.append(node)
        for _, node in graph.out_edges(node):
            stack.append(node)
    return node_titles


arxiv_net_path = "./data/arxiv_network.net"
#arxiv_net_path = "/home/luke/Documents/fax/magistrska/intermediacy/nets/toy.net"

graph = nx.read_pajek(arxiv_net_path)
graph = nx.DiGraph(graph)
#                                                     |
#found = walk(G, "21409", ["16508", "98890", "151774", "113340", "27102", "212", "101855", "140407"], [])
#print(found)

#out = stack_walk(graph, "21409")
#out = stack_walk(graph, "56036")
out = stack_walk_reverse(graph, "80881")

for i in out:
    print(graph.nodes[i])

print("\n----------------------------\n----------------------------\n----------------------------\n")

out = stack_walk(graph, "16508")

for i in out:
    print(graph.nodes[i])



#out = stack_walk(graph, "s")

"""
for node in graph:
    graph.nodes[node]["k_in"] = graph.in_degree(node)
    graph.nodes[node]["k_out"] = graph.out_degree(node)

for i in out:
    print(graph.nodes[i])
"""



def read_input(fname):
    rulesets = []
    with open(fname) as file:
        for line in file:
            rulesets.append(line.split())
    return rulesets

def make_graph(ruleset):
    graph = {}
    for rule in ruleset:
        if "<" in rule:
            a, b = rule.split("<")
        else:
            b, a = rule.split(">")
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
    return graph

def topological_sort(graph):
    visit_order = []
    visited = {c: 0 for c in graph}
    for key in graph:
        if not visited[key]:
            dfs(key, graph, visit_order, visited)
    return visit_order

def dfs(node, graph, visit_order, visited):
    visited[node] = 1
    for next_node in graph[node]:
        if not visited[next_node]:
            dfs(next_node, graph, visit_order, visited)
    visit_order.append(node)

def part1(fname):
    rulesets = read_input(fname)
    res = 0
    for ruleset in rulesets:
        graph = make_graph(ruleset)
        visit_order = topological_sort(graph)
        res+=int("".join(visit_order))
    return res

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part1("input2.txt"))
    print(part1("input3.txt"))
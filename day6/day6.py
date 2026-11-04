def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]

def make_graph(lines):
    graph = {}
    for line in lines:
        parent, children = line.split(":")
        graph[parent] = children.split(",")
    return graph

def invert_graph(graph):
    inverted = {}
    for parent, children in graph.items():
        for child in children:
            if child not in inverted:
                inverted[child] = []
            inverted[child].append(parent)
    return inverted

def dfs(graph, start_node):
    seen = set()
    stack = [start_node]
    while stack:
        curr = stack.pop()
        seen.add(curr)
        if curr not in graph:
            continue
        for child in graph[curr]:
            if child in seen:
                continue
            seen.add(child)
            stack.append(child)
    return seen

def part1(fname):
    ingredients = read_input(fname)
    return len(dfs(make_graph(ingredients), "NULL"))-1

def part2(fname):
    ingredients = read_input(fname)
    graph = invert_graph(make_graph(ingredients))
    return len(dfs(graph, "NULL"))-1

def part3(fname):
    ingredients = read_input(fname)
    graph = invert_graph(make_graph(ingredients))
    null1 = dfs(graph, "NULLv1")
    null2 = dfs(graph, "NULLv2")
    null3 = dfs(graph, "NULLv3")
    null12 = null1.intersection(null2)
    null13 = null1.intersection(null3)
    null23 = null2.intersection(null3)

    null123 = null12.union(null13).union(null23)
    for n in ["NULLv1", "NULLv2", "NULLv3"]:
        if n in null123:
            null123.remove(n)
    return len(null123)


if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))
def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]

def make_graph(lines):
    graph = {}
    energies = {}
    for line in lines:
        cloud_id, start_energy, children = line.split(", ")
        cloud_id = cloud_id.split("=")[-1]
        start_energy = int(start_energy.split("=")[-1])
        energies[cloud_id] = start_energy
        children = children.split("=")[-1].split(",")
        graph[cloud_id] = children
    return graph, energies

def part1(fname, initial_impulse):
    lines = read_input(fname)
    graph, energies = make_graph(lines)
    memory = {}
    start_id = max(graph, key=lambda x: len(graph[x]))
    calculate(start_id, initial_impulse, memory, graph)
    for key, val in memory[(start_id, initial_impulse)].items():
        energies[key]+=val
    return sum(energies.values())



def calculate(node, impulse, memory, graph):
    if (node, impulse) in memory:
        return memory[(node, impulse)]
    res = {key: 0 for key in graph}
    memory[(node, impulse)] = res
    res[node] = impulse
    if impulse==1:
        return res
    for next_node in graph[node]:
        helper = calculate(next_node, impulse-1, memory, graph)
        for key, val in helper.items():
            res[key]+=val
    return res


if __name__=="__main__":
    print(part1("input1.txt", 5))
    print(part1("input2.txt", 10))
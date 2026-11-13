from heapq import heappush, heappop

def index_pairings(n=8):
    all_pairings = set()
    backtrack(n, [], set(), all_pairings)
    return all_pairings

def backtrack(n, curr_pairs, paired_indices, all_pairings):
    if len(curr_pairs)==n//2:
        all_pairings.add(tuple(sorted(curr_pairs)))
        return
    for i in range(n):
        for j in range(i+1, n):
            if i not in paired_indices and j not in paired_indices:
                curr_pairs.append((i, j))
                paired_indices.add(i)
                paired_indices.add(j)
                backtrack(n, curr_pairs, paired_indices, all_pairings)
                paired_indices.remove(j)
                paired_indices.remove(i)
                curr_pairs.pop()

def read_input(fname):
    with open(fname) as file:
        n, edges = file.read().split("\n\n")
        edges = [tuple([int(x)-1 for x in edge.split()]) for edge in edges.split("\n")]
        n = int(n.split(": ")[-1])
    return n, edges

def find_distance_sum(graph, start_node):
    dist = [-1]*len(graph)
    queue = [(start_node, 0)]
    i = 0
    while i<len(queue):
        node, d = queue[i]
        i+=1
        dist[node] = d
        for next_node in graph[node]:
            if dist[next_node]==-1:
                dist[next_node] = d+1
                queue.append((next_node, d+1))
    return dist

def part1(fname):
    n, edges = read_input(fname)
    graph = [[(i+1)%n, (i-1)%n] for i in range(n)]
    res1 = 0
    for i in range(n):
        res1+=sum(find_distance_sum(graph, i))
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    res2 = 0
    for i in range(n):
        dist = find_distance_sum(graph, i)
        res2+=sum(dist)
    return res1-res2

def part2(fname):
    n, edges = read_input(fname)
    graph = [[(i+3)%n, (i+2)%n, (i+1)%n, (i-1)%n, (i-2)%n, (i-3)%n] for i in range(n)]
    route_sum = sum(sum(find_distance_sum(graph, i)) for i in range(n))
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    res = 0
    for i in range(n):
        for j in range(n):
            if abs(i-j)<4 or (i, j) in edges or (j, i) in edges:
                continue
            graph[i].append(j)
            graph[j].append(i)
            route_sum_new = sum((sum(find_distance_sum(graph, k)) for k in range(n)))
            #print(i, j, route_sum_new)
            res = max(res, route_sum-route_sum_new)
            graph[i].pop()
            graph[j].pop()
    return res

def part3(fname):
    all_index_pairings = sorted(list(index_pairings(8)))
    n, edges = read_input(fname)
    graph = [[(i+3)%n, (i+2)%n, (i+1)%n, (i-1)%n, (i-2)%n, (i-3)%n] for i in range(n)]
    route_sum = sum(sum(find_distance_sum(graph, i)) for i in range(n))
    spacing = n//8
    res = 0
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    for i in range(spacing):
        crystal_indices = [(i+d*spacing)%n for d in range(8)]
        for pairing_list in all_index_pairings:
            for a, b in pairing_list:
                x, y = crystal_indices[a], crystal_indices[b]
                graph[x].append(y)
                graph[y].append(x)
            route_sum_new = sum(sum(find_distance_sum(graph, i)) for i in range(n))
            for a, b in pairing_list:
                x, y = crystal_indices[a], crystal_indices[b]
                graph[x].pop()
                graph[y].pop()
            res = max(res, route_sum-route_sum_new)
    return res
    
if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))
    
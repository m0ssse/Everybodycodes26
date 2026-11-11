from heapq import heappush, heappop

def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]

def grow1(growth, limit):
    branches = [0]
    total_size = 0
    splits = 0
    rounds = 0
    while total_size<limit:
        new_branches = []
        for b in branches:
            b+=1
            if b<growth:
                new_branches.append(b)
            else:
                splits+=1
                new_branches.append(b//2)
                new_branches.append(b//2)
                new_branches.append(1)
        branches = new_branches
        total_size = sum(branches)+splits
        rounds+=1
    return rounds, total_size

def grow2(growth, limit):
    branches = [0]
    total_size = 0
    splits = 0
    rounds = 0
    leaves = 1
    while leaves<limit:
        new_branches = []
        for b in branches:
            b+=1
            if b<growth:
                new_branches.append(b)
            else:
                splits+=1
                new_branches.append(b//2)
                new_branches.append(b//2)
                new_branches.append(1)
                leaves+=1
        branches = new_branches
        total_size = sum(branches)+splits
        rounds+=1
    return rounds, total_size

def grow3(growth, limit):
    current_time = 1
    leaves = 1
    heap = [(growth, 1)]
    while leaves<limit:
        current_time = heap[0][0]
        N = 0
        while heap and heap[0][0]==current_time:
            _, n = heappop(heap)
            N+=n
        heappush(heap, (current_time+growth-growth//2, 2*N))
        heappush(heap, (current_time+growth-1, N))
        leaves+=N
    return current_time

def part1(fname):
    lines = read_input(fname)
    res = 0
    for line in lines:
        _, growth, limit = line.split(", ")
        growth = int(growth.split("=")[-1])
        limit = int(limit.split("=")[-1])
        seconds, _ = grow1(growth, limit)
        res+=seconds
    return res

def part2(fname):
    lines = read_input(fname)
    res = 0
    for line in lines:
        _, growth, limit = line.split(", ")
        growth = int(growth.split("=")[-1])
        limit = int(limit.split("=")[-1])
        seconds, _ = grow2(growth, limit)
        res+=seconds
    return res

def part3(fname):
    lines = read_input(fname)
    res = 0
    for line in lines:
        _, growth, limit = line.split(", ")
        growth = int(growth.split("=")[-1])
        limit = int(limit.split("=")[-1])
        seconds = grow3(growth, limit)
        res+=seconds
    return res

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))

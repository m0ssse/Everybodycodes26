def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]
    
def helper1(person):
    return sum(person["parts"].values())

def helper2(person):
    return -len(person["parts"]), sum(person["parts"].values())

def solve(fname, keyfun):
    lines = read_input(fname)
    people = {}
    for line in lines:
        id, q, part, t = [int(s.split("=")[-1]) for s in line.split()]
        if id not in people:
            people[id] = {"parts": {}, "id": id}
        if (q, part) not in people[id]["parts"]:
            people[id]["parts"][(q, part)] = 10**9
        people[id]["parts"][(q, part)] = min(t, people[id]["parts"][(q, part)])
    people_list = list(people.values())
    people_list.sort(key=keyfun)
    return sum((i+1)*sum(person["parts"].values()) for i, person in enumerate(people_list))

def part3(fname):
    lines = read_input(fname)
    score_by_id = {}
    part_rankings = {}
    cumulative_times = {}
    for line in lines:
        id, q, part, t = [int(s.split("=")[-1]) for s in line.split()]
        if id not in cumulative_times:
            cumulative_times[id] = {}
        if q not in cumulative_times[id]:
            cumulative_times[id][q] = [0, 0, 0]
        cumulative_times[id][q][part-1] = t
    for statistics in cumulative_times.values():
        for asd in statistics.values():
            for i in range(3):
                if i and asd[i]:
                    asd[i]+=asd[i-1]
                elif i:
                    break
    part_rankings = {}
    for id, stats in cumulative_times.items():
        for q, times in stats.items():
            for part in range(3):
                if (q, part+1) not in part_rankings:
                    part_rankings[(q, part+1)] = []
                if times[part]:
                    part_rankings[(q, part+1)].append((times[part], id))
    for asd in part_rankings.values():
        asd.sort()

    for (q, part), result_list in part_rankings.items():
        print(f"checking quest {q} part {part}")
        print(f"result list is {result_list}")
        points = 50*part
        for i, (t, id) in enumerate(result_list):
            if not i or t>result_list[i-1][0]:
                points = max(0, 50*part-i)
            if id not in score_by_id:
                score_by_id[id] = 0
            score_by_id[id]+=points
            #print(f"contestant {id} received {points} points")

    final_scores = []
    for i, s in score_by_id.items():
        final_scores.append((s, i))
    final_scores.sort(reverse=True)
    print(final_scores)
    res = 0
    for i, (s, id) in enumerate(final_scores):
        res+=s*(i+1)
    return res

if __name__=="__main__":
    print(solve("input1.txt", helper1))
    print(solve("input2.txt", helper2))
    print(part3("test4.txt"))
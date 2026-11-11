from itertools import chain

class Simulation:
    def __init__(self):
        self.row_dict = {}
        self.diag_pos_dict = {}
        self.diag_neg_dict = {}
        self.rounds = 1

        self.round_dicts = [
            (self.row_dict, 1),
            (self.diag_pos_dict, 1),
            (self.diag_neg_dict, 1),
            (self.row_dict, -1),
            (self.diag_pos_dict, -1),
            (self.diag_neg_dict, -1),
        ]

    def add_ent(self, i, j, ent):
        if i not in self.row_dict:
            self.row_dict[i] = []
        if i-j not in self.diag_pos_dict:
            self.diag_pos_dict[i-j] = []
        if i+j not in self.diag_neg_dict:
            self.diag_neg_dict[i+j] = []
        self.row_dict[i].append(ent)
        self.diag_pos_dict[i-j].append(ent)
        self.diag_neg_dict[i+j].append(ent)

    def round(self):
        h_dict, direction = self.round_dicts[self.rounds%6]
        for h_list in h_dict.values():
            h_list = h_list[::direction]
            curr_h = 0
            for ent in h_list:
                curr_h = ent.grow(curr_h)
        self.rounds+=1
      
class Ent:
    warriors = 0 
    total_energy = 0

    def __init__(self, h, i, j):
        self.h = h
        self.rounds_waited = 0
        self.pos = i, j

    def grow(self, h):
        #print(self, end="")
        if self and self.h>h:
            Ent.total_energy+=1
            h = self.h
            self.h+=1
            #(f" grew to height {self.h}", end="")
            if self.h==10:
                #print(f", became a warrior", end="")
                Ent.warriors+=1
                self.h = 0
                self.rounds_waited = 0
        elif not self:
            self.rounds_waited+=1
        if not self and self.rounds_waited==3:
            self.h = 1
            self.rounds_waited = 0
        #print()
        return h-1

    def __bool__(self):
        return self.h>=1

    def __str__(self):
        return f"ent at {self.pos}, height {self.h}"
        
def read_input(fname):
    with open(fname) as file:
        return [line.strip() for line in file]

def part1(fname):
    grid = read_input(fname)
    diagonals = {}
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char.isnumeric():
                if i-j not in diagonals:
                    diagonals[i-j] = []
                diagonals[i-j].append(int(char))
    res = 0
    for diagonal in diagonals.values():
        curr_height = -1
        for h in diagonal:
            if h>curr_height:
                curr_height = h
                res+=1
            curr_height-=1
    return res

def part2(fname):
    grid = read_input(fname)
    diagonals_pos = {}
    diagonals_neg = {}
    rows = {}
    res = 0
    for i, row in enumerate(grid):
        rows[i] = []
        for j, char in enumerate(row):
            if not char.isnumeric():
                continue
            h = int(char)
            if (i-j) not in diagonals_pos:
                diagonals_pos[i-j] = []
            if (i+j) not in diagonals_neg:
                diagonals_neg[i+j] = []
            rows[i].append(h)
            diagonals_pos[i-j].append(h)
            diagonals_neg[i+j].append(h)
    for height_list in chain(diagonals_pos.values(), diagonals_neg.values(), rows.values()):
        curr_h = 0
        for h in height_list:
            if h>curr_h:
                curr_h = h
                res+=1
            curr_h-=1
        curr_h = 0
        for h in height_list[::-1]:
            if h>curr_h:
                res+=1
                curr_h = h
            curr_h-=1
    return res

def part3(fname):
    grid = read_input(fname)
    sim = Simulation()
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if not char.isnumeric():
                continue
            ent = Ent(int(char), i, j)
            sim.add_ent(i, j, ent)
    while Ent.warriors<100000:    #print(f"round {sim.rounds}")
        sim.round()
        #print(sim.rounds-1, Ent.warriors, Ent.total_energy)
    return Ent.total_energy, sim.rounds
            
if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))
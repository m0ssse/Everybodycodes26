class Ghost:
    id = 1
    directions = {(0, 1): ">", (0, -1): "<", (1, 0): "v", (-1, 0): "^"}
        
    def __init__(self, i, j, di, dj, life=10):
        self.i = i
        self.j = j
        self.di = di
        self.dj = dj
        self.life = life
        self.id = Ghost.id
        Ghost.id+=1

    def get_next_pos(self):
        return self.i+self.di, self.j+self.dj

    def move(self):
        self.i, self.j = self.get_next_pos()

    def turn(self):
        self.di, self.dj = self.dj, -self.di
        return self

    def pos(self):
        return self.j, self.i

    def get_direction(self):
        return self.di, self.dj

    def collide(self, n=1):
        self.life-=n

    def __str__(self):
        return f"G{self.id}, position {self.pos()}, direction {Ghost.directions[self.get_direction()]}, life at {self.life}"

def write_to_log(log_file, rounds, wall_collisions, ghost_collisions, disappeared_ghosts, n, m, walls, occupied, ghosts):
    log_file.write("========================================================================\n")
    log_file.write(f"state after round {rounds}\n")
    log_file.write(f"wall collisions: {', '.join(wall_collisions)}\n")
    log_file.write(f"ghost collisions: {', '.join(ghost_collisions)}\n")
    log_file.write(f"disappeared: {', '.join(disappeared_ghosts)}\n")
    print_grid(n, m, walls, occupied, log_file)
    for ghost in sorted(ghosts, key = lambda x: x.id):
        log_file.write(str(ghost)+"\n")
    log_file.write("\n")

def print_grid(n, m, wall_pos, ghosts, log_file=None):
    grid = []
    for i in range(n):
        grid.append([])
        for j in range(m):
            if (i, j) in wall_pos:
                grid[i].append("#")
            else:
                grid[i].append(".")
    for (i, j), ghost_list in ghosts.items():
        if len(ghost_list)>1:
            grid[i][j] = str(len(ghost_list))
        elif ghost_list:
            grid[i][j] = Ghost.directions[ghost_list[0].get_direction()]
    if log_file is None:
        print("\n".join(["".join(row) for row in grid]))
        print()
    else:
        log_file.write("\n".join(["".join(row) for row in grid])+"\n\n")


def read_input(fname, initial_life):
    wall_pos = set()
    ghosts = []
    n = 0
    with open(fname) as file:
        for i, row in enumerate(file):
            n+=1
            m=0
            for j, c in enumerate(row.strip()):
                m+=1
                if c=="#":
                    wall_pos.add((i, j))
                elif c=="^":
                    ghosts.append(Ghost(i, j, -1, 0, initial_life))
                elif c==">":
                    ghosts.append(Ghost(i, j, 0, 1, initial_life))
                elif c=="v":
                    ghosts.append(Ghost(i, j, 1, 0, initial_life))
                elif c=="<":
                    ghosts.append(Ghost(i, j, 0, -1, initial_life))
    return wall_pos, ghosts, n, m

def part1(fname, initial_life = 10):
    Ghost.id = 1
    walls, ghosts, _, _ = read_input(fname, initial_life)
    collisions = 0
    for _ in range(10):
        occupied = {}
        for ghost in ghosts:
            if ghost.get_next_pos() in walls:
                collisions+=1
                ghost.turn()
            else:
                ghost.move()
            if ghost.pos() not in occupied:
                occupied[ghost.pos()] = []
            occupied[(ghost.pos())].append(ghost)
        for ghosts_in_pos in occupied.values():
            if len(ghosts_in_pos)>1:
                collisions+=len(ghosts_in_pos)
                for ghost in ghosts_in_pos:
                    ghost.turn().turn()
    return collisions

def part2(fname, disappear_threshold, logging=True):
    Ghost.id = 1
    walls, ghosts, n, m = read_input(fname, disappear_threshold)
    rounds = 0
    if logging:
        log_file = open("log.txt", "w")
    while ghosts:
        rounds+=1
        occupied = {}
        new_ghosts = []
        disappeared_ghosts = []
        wall_collisions = []
        ghost_collisions = []
        for ghost in ghosts:
            if ghost.get_next_pos() in walls:
                ghost.turn()
                ghost.collide()
                wall_collisions.append(f"G{ghost.id}")
            else:
                ghost.move()
            if ghost.pos() not in occupied:
                occupied[ghost.pos()] = []
            if ghost.life>0:
                occupied[(ghost.pos())].append(ghost)
            else:
                disappeared_ghosts.append(f"G{ghost.id}")
        for ghosts_in_pos in occupied.values():
            for ghost in ghosts_in_pos:
                if len(ghosts_in_pos)>1:
                    ghost.turn().turn()
                    ghost_collisions.append(f"G{ghost.id}")
                    ghost.collide()
                if ghost.life>0:
                    new_ghosts.append(ghost)
                else:
                    disappeared_ghosts.append(f"G{ghost.id}")
        ghosts = new_ghosts
        if logging:
            write_to_log(log_file, rounds, wall_collisions, ghost_collisions, disappeared_ghosts, n, m, walls, occupied, ghosts)
    if logging:
        log_file.close()
    return rounds

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt", 10**4, logging=False))
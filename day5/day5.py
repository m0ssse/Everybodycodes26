def read_input(fname):
    with open(fname) as file:
        return [[int(x) for x in row.strip()] for row in file]

def get_neighbs(i, j, n, m):
    res = []
    for ii in range(i-1, i+2):
        for jj in range(j-1, j+2):
            if ii==i and jj==j or ii<0 or ii>=n or jj<0 or jj>=m:
                continue
            res.append((ii, jj))
    return res

def get_neighbs2(i, j):
    res = []
    for ii in range(i-2, i+3):
        for jj in range(j-2, j+3):
            if (ii==i and jj==j) or (ii==i-2 and jj==j-2) or (ii==i-2 and jj==j+2) or (ii==i+2 and jj==j-2) or (ii==i+2 and jj==j+2):
                continue
            res.append((ii, jj))
    return res
            

def print_grid(grid, land):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in land:
                print("#", end="")
            else:
                print(".", end="")
        print()

def print_grid2(grid, land, sand):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in sand:
                print("=", end="")
            elif (i, j) in land:
                print("#", end="")
            else:
                print(".", end="")
        print()

def print_grid3(grid, land, sand, trees):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (i, j) in trees:
                print("@", end="")
            elif (i, j) in sand:
                print("=", end="")
            elif (i, j) in land:
                print("#", end="")
            else:
                print(".", end="")
        print()

def get_land_cells(grid):
    n, m = len(grid), len(grid[0])
    edge_cells = set(get_neighbs(n//2, m//2, n, m))
    land_cells = set([(n//2, m//2)])
    cells_added = True
    while cells_added:
        cells_added = False
        new_land_cells = set()
        for i, j in edge_cells:
            neighb_count = 0
            for ii, jj in get_neighbs(i, j, n, m):
                if grid[ii][jj] or (ii, jj) in land_cells:
                    neighb_count+=1
            if neighb_count>=5:
                new_land_cells.add((i, j))
                cells_added = True

        for i, j in new_land_cells:
            land_cells.add((i, j))
            edge_cells.remove((i, j))

        for i, j in new_land_cells:
            for ii, jj in get_neighbs(i, j, n, m):
                if (ii, jj) not in land_cells:
                    edge_cells.add((ii, jj))
    #print_grid(grid, land_cells)
    return land_cells

def get_sand_cells(grid, land_cells):
    n, m = len(grid), len(grid[0])
    sand_cells = set()
    for i, j in land_cells:
        if i==0 or i==n-1 or j==0 or j==m-1:
            sand_cells.add((i, j))
            continue
        for ii, jj in get_neighbs(i, j, n, m):
            if (ii, jj) not in land_cells:
                sand_cells.add((i, j))
                break
    edge_cells = set()
    for i, j in sand_cells:
        for ii, jj in get_neighbs(i, j, n, m):
            if (ii, jj) in land_cells and (ii, jj) not in sand_cells:
                edge_cells.add((ii, jj))

    cells_added = True
    while cells_added:
        cells_added = False
        sand_cells_new = set()
        for i, j in edge_cells:
            neighb_count = 0
            for ii, jj in get_neighbs(i, j, n, m):
                if (ii, jj) in sand_cells:
                    neighb_count+=1
            if neighb_count>=5:
                sand_cells_new.add((i, j))
                cells_added = True

        for i, j in sand_cells_new:
            sand_cells.add((i, j))
            edge_cells.remove((i, j))

        for i, j in sand_cells_new:
            for ii, jj in get_neighbs(i, j, n, m):
                if (ii, jj) not in sand_cells and (ii, jj) in land_cells:
                    edge_cells.add((ii, jj))

    return sand_cells

def get_tree_cells(grid, land_cells, sand_cells):
    n, m = len(grid), len(grid[0])
    tree_cells = set()
    land_cells = land_cells.difference(sand_cells)
    for i, j in land_cells:
        for ii, jj in get_neighbs2(i, j):
            if (ii, jj) not in land_cells:
                break
        else:
            tree_cells.add((i, j))

    for i, j in tree_cells:
        land_cells.remove((i, j))

    for _ in range(2):
        trees_new = set()
        for i, j in land_cells:
            tree_neighbs = 0
            for ii, jj in get_neighbs(i, j, n, m):
                if (ii, jj) in sand_cells:
                    break
                elif (ii, jj) in tree_cells:
                    tree_neighbs+=1
            else:
                if tree_neighbs>=4:
                    trees_new.add((i, j))
        for i, j in trees_new:
            land_cells.remove((i, j))
            tree_cells.add((i, j))

    return tree_cells


def part1(fname):
    grid = read_input(fname)
    return len(get_land_cells(grid))

def part2(fname):
    grid = read_input(fname)
    land_cells = get_land_cells(grid)
    sand_cells = get_sand_cells(grid, land_cells)
    return len(sand_cells)

def part3(fname):
    grid = read_input(fname)
    land_cells = get_land_cells(grid)
    sand_cells = get_sand_cells(grid, land_cells)
    tree_cells = get_tree_cells(grid, land_cells, sand_cells)
    return len(tree_cells)

    

if __name__=="__main__":
    print(part1("input1.txt"))
    print(part2("input2.txt"))
    print(part3("input3.txt"))
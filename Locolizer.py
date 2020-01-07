R = 'r'
G = 'g'
grid = [[G,G,G],
        [G,R,G],
        [G,G,G]]
color = R
p = 1/9
p_hit = 3
p_miss = 1
blur = 0.03

def initialize_beliefs(grid):
    height = len(grid)
    width = len(grid[0])
    area = height * width
    belief_per_cell = 1 / area # uniform distribution
    beliefs = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(belief_per_cell)
        beliefs.append(row)
    return beliefs

def sense(color, grid, beliefs, p_hit, p_miss):
    new_beliefs = []
    s = 0 # sum of all elements in grid
    for i in range(len(grid)):
        new_beliefs.append([])
        for j in range(len(grid[0])):
            # multiply p_hit if same as measurement
            if grid[i][j] == color:
                new_beliefs[i].append(beliefs[i][j]*p_hit)
                s += beliefs[i][j]*p_hit
            # multiply p_miss if not same as measurement
            else:
                new_beliefs[i].append(beliefs[i][j]*p_miss)
                s += beliefs[i][j]*p_miss
    # normalize: divide each element by the sum of all emelents
    for i in range(len(new_beliefs)):
        for j in range(len(new_beliefs[0])):
            new_beliefs[i][j] /= s
    return new_beliefs

def move(dy, dx, beliefs, blurring):
    height = len(beliefs)
    width = len(beliefs[0])
    new_G = [[0 for i in range(width)] for j in range(height)]
    for i, row in enumerate(beliefs):
        for j, cell in enumerate(row):
            new_i = (i + dy ) % height
            new_j = (j + dx ) % width
            new_G[int(new_i)][int(new_j)] = cell
    return blur(new_G, blurring)

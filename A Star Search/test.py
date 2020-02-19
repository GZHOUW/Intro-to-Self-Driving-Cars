import PathPlanner
from helpers import load_map_40

map_40 = load_map_40()
planner = PathPlanner.PathPlanner(map_40, 5, 34)
path = planner.path
if path == [5, 16, 37, 12, 34]:
    print("great! Your code works for these inputs!")
else:
    print("something is off, your code produced the following:")
    print(path)
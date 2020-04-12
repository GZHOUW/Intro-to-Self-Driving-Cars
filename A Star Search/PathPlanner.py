# Use A* search to implement a "Google-maps" style route planning algorithm.
import math

class PathPlanner():
    def __init__(self, M, start, goal):
        self.map = M  # map= {0: {'pos': (0.781, 0.494), 'connections': [36, 34, 17]}
        self.start = start
        self.goal = goal
        self.explored = self.create_explored()
        self.frontier = self.create_frontier()
        self.paths = self.create_paths()  # holds the previous nodes that best reaches a given node
        # paths = {3:[0,1,2], 15:[5,6,7,3]}
        self.gScore = self.create_gScore()
        self.fScore = self.create_fScore()
        self.bestPath = self.run_search()

    def reconstruct_path(self, current):  # takes in current node
        """ Reconstructs bestPath after search """
        total_path = [current] # e.g.  [45]
        while current in self.paths.keys():
            current = self.paths[current]
            total_path.append(current)
        return total_path

    def run_search(self):
        while not self.is_frontier_empty():  # keep searching until there is nothing in the frontier
            current = self.get_best_node()  # choose the node with lowest f score from the frontier
            if current == self.goal:
                self.bestPath = [x for x in reversed(self.reconstruct_path(current))]
                return self.bestPath # end function
            else:
                self.frontier.remove(current)  # remove current node from frontier
                self.explored.add(current)  # add current node to explored

            for neighbor in self.get_neighbors(current):
                if neighbor in self.explored:
                    continue  # Ignore the neighbor which is already evaluated.

                if not neighbor in self.frontier:  # Discover a new node
                    self.frontier.add(neighbor) # add it to frontier

                if self.get_tentative_gScore(current, neighbor) >= self.get_gScore(neighbor):
                    continue  # This is not a better path.
                else:
                    # This Path is the best until now. Record it!
                    self.record_path(current, neighbor)
        print("No best path Found")
        self.bestPath = None
        return False

    def create_explored(self):
        return set()

    def create_frontier(self):
        # a set, initially, only the start node is known.
        return {self.start}  # a set

    def create_paths(self):
        """Creates and returns a data structure that shows which node can most efficiently be reached from another, for each node."""
        return dict()

    def create_gScore(self):
        """Creates and returns a data structure that holds the cost of getting from the start node to that node,
        for each node. The cost of going from start to start is zero. The cost of going from start to start is zero.
        The rest of the node's values should be set to infinity. """
        g_dict = dict()
        nodes = self.map.keys()
        for node in nodes:
            if node == self.start:
                g_dict[node] = 0
            else:
                g_dict[node] = math.inf
        return g_dict

    def create_fScore(self):
        """Creates a dictionary that holds the f score for each node. total cost of getting from the start node to the goal
        For the first node, f score is the distance"""
        f_dict = dict()
        nodes = self.map.keys()
        for node in nodes:
            if node == self.start:
                f_dict[node] = self.distance(self.start, self.goal)
            else:
                f_dict[node] = math.inf
        return f_dict

    def is_frontier_empty(self):
        """returns True if the frontier is empty. False otherwise. """
        return len(self.frontier) == 0

    def get_best_node(self):
        """ Returns the node in the frontier with the lowest value of f(node)."""
        i = 0
        for n in self.frontier:
            if i == 0:
                f_min = self.get_fScore(n)
                node_min = n
            else:
                f = self.get_fScore(n)
                if f < f_min:
                    f_min = f
                    node_min = n
            i += 1
        return node_min

    def get_neighbors(self, node):
        """Returns the neighbors of a node"""
        return self.map[node]['connections']

    def distance(self, node1, node2):
        """ Computes the Euclidean L2 Distance"""
        x1 = self.map[node1]['pos'][0]
        y1 = self.map[node1]['pos'][1]
        x2 = self.map[node2]['pos'][0]
        y2 = self.map[node2]['pos'][1]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def get_gScore(self, node):
        # Returns the g Score of a node
        return self.gScore[node]

    def get_tentative_gScore(self, current, neighbor):
        # Return the g Score of the current node
        # plus distance from the current node to it's neighbors
        return self.get_gScore(current) + self.distance(current, neighbor)

    def get_hScore(self, node):
        return self.distance(node, self.goal)

    def get_fScore(self, node):
        """Calculate the f score of a node. """
        # F = G + H
        return self.get_gScore(node) + self.get_hScore(node)

    def record_path(self, current, neighbor):
        """ Record the best Path to a node, by updating paths, gScore, and fScore """
        self.paths[neighbor] = current
        self.gScore[neighbor] = self.get_tentative_gScore(current, neighbor)
        self.fScore[neighbor] = self.get_fScore(current)

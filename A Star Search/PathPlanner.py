# Use A* search to implement a "Google-maps" style route planning algorithm.
import math


class PathPlanner():
    def __init__(self, M, start, goal):
        self.map = M
        self.start = start
        self.goal = goal
        self.explored = self.create_explored() #if goal != None and start != None else None
        self.frontier = self.create_frontier() #if goal != None and start != None else None
        self.cameFrom = self.create_cameFrom() # if goal != None and start != None else None
        self.gScore = self.create_gScore() #if goal != None and start != None else None
        self.fScore = self.create_fScore() #if goal != None and start != None else None
        self.path = self.run_search() #if self.map and self.start != None and self.goal != None else None

    def reconstruct_path(self, current):
        """ Reconstructs path after search """
        total_path = [current]
        while current in self.cameFrom.keys():
            current = self.cameFrom[current]
            total_path.append(current)
        return total_path

    def run_search(self):
        self.explored = self.explored #if self.explored != None else self.create_explored()
        self.frontier = self.frontier #if self.frontier != None else self.create_frontier()
        self.cameFrom = self.cameFrom #if self.cameFrom != None else self.create_cameFrom()
        self.gScore = self.gScore #if self.gScore != None else self.create_gScore()
        self.fScore = self.fScore #if self.fScore != None else self.create_fScore()

        while not self.is_frontier_empty():
            current = self.get_current_node()

            if current == self.goal:
                self.path = [x for x in reversed(self.reconstruct_path(current))]
                return self.path
            else:
                self.frontier.remove(current)
                self.explored.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor in self.explored:
                    continue  # Ignore the neighbor which is already evaluated.

                if not neighbor in self.frontier:  # Discover a new node
                    self.frontier.add(neighbor)

                # The distance from start to a neighbor
                # the "dist_between" function may vary as per the solution requirements.
                if self.get_tentative_gScore(current, neighbor) >= self.get_gScore(neighbor):
                    continue  # This is not a better path.

                # This path is the best until now. Record it!
                self.record_best_path_to(current, neighbor)
        print("No Path Found")
        self.path = None
        return False

    def create_explored(self):
        # Creates and returns a data structure suitable to hold the set of nodes already evaluated
        return set()

    def create_frontier(self):
        # a set, initially, only the start node is known."""
        return {self.start}  # a set

    def create_cameFrom(self):
        """Creates and returns a data structure that shows which node can most efficiently be reached from another, for each node."""
        return {}

    def create_gScore(self):
        """Creates and returns a data structure that holds the cost of getting from the start node to that node,
        for each node. The cost of going from start to start is zero. The cost of going from start to start is zero.
        The rest of the node's values should be set to infinity. """
        g_dict = {}
        nodes = self.map.keys()
        for node in nodes:
            if node == self.start:
                g_dict[node] = 0
            else:
                g_dict[node] = math.inf
        return g_dict

    def create_fScore(self):
        """Creates and returns a data structure that holds the total cost of getting from the start node to the goal
        by passing by that node, for each node. That value is partly known, partly heuristic.
        For the first node, that value is completely heuristic."""
        f_dict = {}
        nodes = self.map.keys()
        for node in nodes:
            if node == self.start:
                f_dict[node] = self.distance(self.start, self.goal)
            else:
                f_dict[node] = math.inf
        return f_dict

    def is_frontier_empty(self):
        """returns True if the open set is empty. False otherwise. """
        return len(self.frontier) == 0

    def get_current_node(self):
        """ Returns the node in the open set with the lowest value of f(node)."""
        i = 0
        for n in self.frontier:
            if i == 0:
                f_min = self.calculate_fScore(n)
                node_min = n
            else:
                f = self.calculate_fScore(n)
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
        # Return the heuristic cost estimate of a node
        return self.distance(node, self.goal)

    def calculate_fScore(self, node):
        """Calculate the f score of a node. """
        # F = G + H
        return self.get_gScore(node) + self.get_hScore(node)

    def record_best_path_to(self, current, neighbor):
        """ Record the best path to a node, by updating cameFrom, gScore, and fScore """
        self.cameFrom[neighbor] = current
        self.gScore[neighbor] = self.get_tentative_gScore(current, neighbor)
        self.fScore[neighbor] = self.calculate_fScore(current)

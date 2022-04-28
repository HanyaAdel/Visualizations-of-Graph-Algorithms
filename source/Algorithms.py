import sys


class Algorithms:
    graph = []
    found = False
    visited_return = []     # visited list to be returned
    visited = []            # visited list to prevent infinite loops
    path = []

    def __init__(self, num_nodes, graph):
        self.graph = graph
        self.found = False
        self.visited_return = [False for i in range(num_nodes)]
        self.visited = [False for i in range(num_nodes)]
        self.path = []

    def get_visited(self):
        return self.visited_return

    def get_path(self):
        return self.path

    def reset(self):
        for i in self.visited:
            i = False
        self.path = []

    def depth_limited(self, source, goal, max_depth, depth=0):
        self.path.append(source)
        self.visited_return[source] = True
        if source == goal:
            self.found = True
            return
        if depth != max_depth:
            for child in self.graph[source]:
                if not self.visited[child]:
                    self.visited[child] = True
                    self.depth_limited(child, goal, max_depth, depth + 1)
                    if self.found:
                        return
                    self.visited[child] = False

        self.path.pop()

    def dfs(self, source, goal):
        return self.depth_limited(source, goal, sys.maxsize)

    def iterative_deepening(self, source, goal, max_depth):
        for depth in range(max_depth):
            self.reset()
            self.depth_limited(source, goal, depth)
            if self.found:
                return

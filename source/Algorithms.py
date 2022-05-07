import sys
from Graph import Node, nodes, adj_list


class Algorithms:
    found = False
    visited_return = []     # visited list to be returned
    visited_flag = {}       # to avoid duplicates in visited_return (also consider using ordered sets to eliminate this)
    visited = {}            # visited list to prevent infinite loops
    visited_path = []       # list to be used for illustrating the algorithm path on the graph
    path = []

    def __init__(self):
        self.reset()

    def reset(self):
        self.clear_visited_return()
        self.reset_iterative_deepening()
        self.visited_path.clear()

    def clear_visited_return(self):
        self.visited_return.clear()
        for node in nodes:
            self.visited_flag[node] = False

    def reset_iterative_deepening(self):
        self.path.clear()
        self.found = False
        for node in nodes:
            self.visited[node] = False

    def get_visited(self):
        return self.visited_return

    def get_path(self):
        return self.path

    def get_visited_path(self):
        return self.visited_path

    def depth_limited(self, source: Node, goal: Node, max_depth, depth=0):
        self.path.append(source.name)
        self.visited_path.append(source.name)
        self.visited[source] = True

        if not self.visited_flag[source]:
            self.visited_return.append(source.name)
            self.visited_flag[source] = True

        if source == goal:
            self.found = True
            return
        if depth != max_depth:
            for child in adj_list[source]:
                child_node = child[0]
                if not self.visited[child_node]:
                    # self.visited[child_node] = True
                    self.depth_limited(child_node, goal, max_depth, depth + 1)
                    if self.found:
                        return
                    self.visited[child_node] = False

        self.path.pop()

    def dfs(self, source, goal):
        return self.depth_limited(source, goal, sys.maxsize)

    def iterative_deepening(self, source, goal, max_depth):
        for depth in range(max_depth):
            self.reset_iterative_deepening()
            self.depth_limited(source, goal, depth)
            if self.found:
                return

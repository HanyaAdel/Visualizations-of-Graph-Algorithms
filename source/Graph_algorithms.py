from queue import PriorityQueue


class Algorithms:
    graph = []
    found = False
    visited_return = []     # visited list to be returned
    visited = []            # visited list to prevent infinite loops
    path = []
    queue = []              #queue for bfs function
    solutionPath = []
    parent = []
    heuristics = []

    def __init__(self, num_nodes, graph):
        self.graph = graph
        self.found = False
        self.visited_return = [False for i in range(num_nodes)]
        self.visited = [False for i in range(num_nodes)]
        self.parent = [0 for i in range(num_nodes)]
        self.path = []
        self.solutionPath = []
        self.queue = []
        self.heuristics = []

    def get_visited(self):
        return self.visited_return

    def get_solution_path(self):
        return self.solutionPath

    def generate_solution_path(self, source, goal):
        node = goal
        self.solutionPath.append(node)
        while node != source:
            node = self.parent[node]
            self.solutionPath.append(node)

        self.solutionPath.reverse()
        return

    def bfs(self, source, goal):
        self.visited_return[source] = True
        self.queue.append(source)

        while self.queue:          # Creating loop to visit each node
            frontNode = self.queue.pop(0) 
            
            if frontNode == goal:
                self.generate_solution_path(source, goal)
                self.found = True
                return
            
            for child in self.graph[frontNode]:
                if not self.visited_return[child]:
                     self.visited_return[child] = True
                     self.parent[child] = frontNode
                     self.queue.append(child)


    def greedy_best_first_search(self, source, goal, heuristics):
        self.heuristics = heuristics
        self.visited_return[source] = True

        pq = PriorityQueue()
        pq.put((self.heuristics[source], source))
        
        while pq.empty() == False:
            topNode = pq.get()[1]

            if topNode == goal:
                self.generate_solution_path(source, goal)
                return
    
            for childNode in self.graph[topNode]:
                if self.visited_return[childNode] == False:
                    self.visited_return[childNode] = True
                    self.parent[childNode] = topNode
                    pq.put((self.heuristics[childNode], childNode))
        

from dis import dis
import sys
from tkinter import TOP
from Graph import Node, nodes, adj_list
from queue import PriorityQueue


class Algorithms:
    found = False
    START_NODE = 0          # start node for calculating solution path for depth limited based algorithms
    visited_return = []     # visited list to be returned
    visited_return_ID = []  # visited list to be returned for iterative deepening algorithm
    visited_flag = {}       # to avoid duplicates in visited_return (also consider using ordered sets to eliminate this)
    visited = {}            # visited list to prevent infinite loops
    visited_path = []       # list to be used for illustrating the algorithm path on the graph
    path = []
    parent = {}             #to generate solution path 
    totalCost = 0           #returns total cost from source to destination

    def __init__(self):
        self.reset()

    def reset(self):
        self.totalCost = 0; 
        self.clear_visited_return()
        self.reset_iterative_deepening()
        self.parent.clear()
        self.visited_path.clear()
        self.visited_return_ID.clear()

    def clear_visited_return(self):
        self.visited_return.clear()
        self.reset_visited_flag()

    def reset_visited_flag(self):
        for node in nodes:
            self.visited_flag[node] = False

    def reset_visited(self):
        for node in nodes:
            self.visited[node] = False

    def reset_iterative_deepening(self):
        self.path.clear()
        self.found = False
        self.reset_visited()
        self.clear_visited_return()

    def get_visited(self):
        return self.visited_return

    def get_visited_ID(self):                   # get visited lists for Iterative Deepening
        return self.visited_return_ID

    def get_path(self):
        return self.path

    def get_visited_path(self):
        return self.visited_path

    def get_total_cost(self):
        return self.totalCost


    def isGoalNode (self, currNode: Node, goalNodes = []):
        for node in goalNodes:
            if (currNode == node):
                self.found = True
                return True
        return False

    def depth_limited(self, source: Node, goalNodes, max_depth, depth=0):
        #self.path.append(source.name)
        self.visited_path.append(source.name)
        self.visited[source] = True

        if not self.visited_flag[source]:
            self.visited_return.append(source.name)
            self.visited_flag[source] = True

        if self.isGoalNode(source, goalNodes):
            self.found = True
            self.generate_solution_path_and_calculate_total_cost(self.START_NODE,source)
            return
        if depth != max_depth:
            for child in adj_list[source]:
                child_node = child[0]
                edge_weight = child[1]
                if not self.visited[child_node]:
                    self.parent[child_node] = [source, edge_weight]
                    # self.visited[child_node] = True
                    self.depth_limited(child_node, goalNodes, max_depth, depth + 1)
                    if self.found:
                        return
                    self.visited[child_node] = False

        #self.path.pop()

    def dfs(self, source, goal):
        return self.depth_limited(source, goal, sys.maxsize)

    def iterative_deepening(self, source, goal):
        for depth in range(len(nodes)):                         # maximum possible depth is if the nodes are in a line
            self.reset_iterative_deepening()
            self.depth_limited(source, goal, depth)
            visited = self.visited_return.copy()
            self.visited_return_ID.append(visited)
            if self.found:
                return


    def generate_solution_path_and_calculate_total_cost(self, source:Node, goal:Node):
        node = [goal, 0]
        self.path.append(node[0].name)
       
        while node[0] != source:
            node = self.parent[node[0]]
            self.path.append(node[0].name)
            self.totalCost+= node[1]
        self.path.reverse()
       
        return

    def bfs(self, source: Node, goalNodes = []):
        queue = []              #queue for bfs function
        queue.append(source)
        self.visited_flag[source] = True
        self.visited_return.append(source.name)
        
        while queue:          # Creating loop to visit each node
            frontNode = queue.pop(0) 
            self.visited_path.append(frontNode.name)
            
            if not self.visited_flag[frontNode]:
                self.visited_flag[frontNode] = True
                self.visited_return.append(frontNode.name)

            if self.isGoalNode(frontNode, goalNodes):
                self.generate_solution_path_and_calculate_total_cost(source, frontNode)
                return
            
            for child in adj_list[frontNode]:
                if not self.visited_flag[child[0]]:
                    self.parent[child[0]] = [frontNode, child[1]]
                    queue.append(child[0])


    def greedy_best_first_search(self, source: Node, goalNodes = []):

        self.visited_flag[source] = True
        self.visited_return.append(source.name)

        pq = PriorityQueue()
        pq.put((source.heuristic, source.name))
        
        while pq.empty() == False:
            topNode = Node.get_node(pq.get()[1])
            self.visited_path.append(topNode.name)

            if self.visited_flag[topNode] == False:
                self.visited_flag[topNode] = True
                self.visited_return.append(topNode.name)

            if self.isGoalNode(topNode, goalNodes):
                self.generate_solution_path_and_calculate_total_cost(source, topNode)
                return
    
            for childNode in adj_list[topNode]:
                if self.visited_flag[childNode[0]] == False:

                    self.parent[childNode[0]] = [topNode, childNode[1]]
                    pq.put((childNode[0].heuristic, childNode[0].name))

    def A_star_search(self, source: Node, goalNodes=[]):
        open_list = set([source.name])
        closed_list = set([])
        g = {}

        g[source] = 0

        while len(open_list) > 0:
            node = None

            # find node with smallest value of f()
            for n in open_list:
                m = Node.get_node(n)
                if node == None or g[m] + m.heuristic < g[node] + node.heuristic:
                    node = m

            # if node == None:
            #  print('Path does not exist!')
            # return None
            self.visited_flag[node] = True
            self.visited_return.append(node.name)
            self.visited_path.append(node.name)

            if (self.isGoalNode(node, goalNodes)):
                self.generate_solution_path_and_calculate_total_cost(source, node)
                return

            # expand node
            for childNode in adj_list[node]:
                # if node isn't traversed before, add it to fringe
                if childNode[0].name not in open_list and childNode[0].name not in closed_list:
                    open_list.add(childNode[0].name)
                    self.parent[childNode[0]] = [node, childNode[1]]
                    g[childNode[0]] = g[node] + childNode[1]

                else:
                    # if node is in fringe and reached with smaller g() then update it
                    if g[childNode[0]] > g[node] + childNode[1]:
                        g[childNode[0]] = g[node] + childNode[1]
                        self.parent[childNode[0]] = [node, childNode[1]]

                        # if node was in closed list, remove it and add to open list to be
                        # traversed with new g()
                        if childNode[0].name in closed_list:
                            closed_list.remove(childNode[0].name)
                            open_list.add(childNode[0].name)

            # finished expanding node and adding it to closed list
            open_list.remove(node.name)
            closed_list.add(node.name)
    
    def uniform_cost(self, source: Node, goalNodes= []):
    
        dist = {}
        for node in nodes:
            dist[node] = int(sys.maxsize)
    
        pq = PriorityQueue()
        dist[source] = 0
        pq.put((0, source.name))

        while pq.empty() == False:
            top = pq.get()
            topNode =  Node.get_node(top[1])
            currCost = top[0]
           
            if (currCost > dist[topNode]):
                continue
            self.visited_path.append(topNode.name)

            if not self.visited_flag[topNode]:
                self.visited_return.append(topNode.name)
                self.visited_flag[topNode] = True


            if self.isGoalNode(topNode, goalNodes):
                   self.generate_solution_path_and_calculate_total_cost(source, topNode)
                   return

            for child in adj_list[topNode]:
                if currCost + child[1] < dist[child[0]]:
                    dist[child[0]] = currCost + child[1]
                    pq.put((dist[child[0]], child[0].name))
                    self.parent[child[0]] = [topNode, child[1]]



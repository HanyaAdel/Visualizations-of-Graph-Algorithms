from Algorithms import Algorithms
from Graph import Node, nodes, adj_list

import sys

n = int(input("Enter number of nodes: "))
m = int(input("Enter number of edges: "))

print('Entering Nodes:')

for i in range(n):
    node_name = str(input("Enter node name: "))
    node_heuristic = 1              # modify this for user defined heuristics
    node = Node(node_name,node_heuristic)
    nodes.append(node)

print("Entering edges")

for i in range(m):
    x = str(input("Enter source node: "))
    y = str(input("Enter destination node: "))
    weight = 1                      # modify this for user defined weights
    src = Node.get_node(x)
    dest = Node.get_node(y)
    temp = [dest, weight]
    adj_list[src].append(temp)
    temp2 = [src, weight]
    adj_list[dest].append(temp2)    # because I am using undirected graphs


alg = Algorithms()
source = Node.get_node(str(input("Enter Source: ")))
goal = Node.get_node(str(input("Enter Goal: ")))
# alg.dfs(source, goal)
# alg.depth_limited(source, goal, sys.maxsize)
alg.iterative_deepening(source, goal, sys.maxsize)
v = alg.get_visited()
path = alg.get_path()
visited_path = alg.get_visited_path()
print("Visited:", v)
print("Solution Path:", path)
print("Visited Path", visited_path)

# Todo add a function to find the max depth of the given graph (given the source node of the tree)

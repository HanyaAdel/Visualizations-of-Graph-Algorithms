import heapq
import sys
from Graph_Input import Node, nodes, adj_list
from queue import PriorityQueue

def dijkstra(source: Node, goal: Node):
    #self.visited_flag[source] == True
    #self.visited_return.append(source.name)
    dist = {}
    for node in nodes:
        dist[node] = int(sys.maxsize)
 
    pq = PriorityQueue()
    pq.put((0, source))
    dist[source] = 0
        
    while pq.empty() == False:
        topNode = pq.get()[1]
        currCost = pq.ger()[0] 

        if (currCost > dist[topNode]):
            continue
        #self.visited_path.append(topNode.name)

        #if not self.visited_flag[topNode]:
        #    self.visited_return.append(topNode.name)
        #    self.visited_flag[topNode] = True


        #if topNode == goal:
        #       self.generate_solution_path_and_calculate_total_cost(source, goal)
        #       self.found = True
        #       return

        for child in adj_list[topNode]:
            if currCost + child[1] < dist[child[0]]:
                dist[child[0]] = currCost + child[1]
                pq.put(dist[child[0]], child[0])
                #self.parent[childNode[0]] = [topNode, childNode[1]]
    
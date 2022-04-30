import heapq
import sys
from Graph_Input import nodes, adj_list

def dijkstra(start):
    print("called")

    dist = {}
    visited = {}
    for node in nodes:
        dist[node] = int(sys.maxsize)
        visited[node] = False
    

    dist[start] = 0

    pq = [(0, start)]
    

    while len(pq) > 0:
        _, topNode = heapq.heappop(pq)

        if visited[topNode]:
            continue

        visited[topNode] = True

        for child in adj_list[topNode]:
            print (child[0].name, "       ", child[1])
            if dist[topNode] + child[1] < dist[child[0]]:
                dist[child[0]] = dist[topNode] + child[1]
                heapq.heappush(pq, (dist[child[0]], child[0]))
    for num in dist:
        print(num.name, "    ", dist[num])
    return dist


dijkstra (nodes[0])

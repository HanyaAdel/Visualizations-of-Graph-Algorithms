from collections import defaultdict

adj_list = defaultdict(list)
nodes = []


class Node:
    def __init__(self, name: str, heuristic: int):
        self.name = name
        self.heuristic = heuristic

    @staticmethod
    def get_node(name: int):
        for node in nodes:
            if node.name == name:
                return node

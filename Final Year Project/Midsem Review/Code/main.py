import pandas as pd
import random
from collections import defaultdict

# create the graph node
class Node():
    def __init__(self, coordinates, name):
        self.coordinates = coordinates
        self.name = name
        self.neighbors = set()
        self.charge = False
    
    def get_name(self):
        return self.name

    def get_coordinates(self):
        return self.coordinates
    
    def is_charging_station(self):
        return self.charge
    
    # if the node is a charging station, set the power and cost
    def set_charging_station(self, power, cost):
        self.charge = True
        self.power = power
        self.cost = cost
    
    # we get the charging info if the node is a charging station
    def get_charging_info(self):
        if not self.charge:
            return None
        return [self.power, self.cost]

# create the graph
class Graph():
    def __init__(self):
        self.nodes = set()
        self.coordinates = {}
        self.distance = defaultdict(dict)
        self.time = defaultdict(dict)
        self.get_node = {}
        self.names = set()

    def add_node(self, coordinates, name):
        node = Node(coordinates, name)
        self.nodes.add(node)
        self.names.add(name)
        self.coordinates[name] = coordinates
        self.get_node[name] = node
    
    def add_edge(self, node1, node2, distance):
        node1.neighbors.add(node2)
        node2.neighbors.add(node1)
        self.distance[node1][node2] = distance
        self.distance[node2][node1] = distance
        self.time[node1][node2] = distance
        self.time[node2][node1] = distance

    # find the shortest path between two nodes
    def shortest_path(self, source, destination):
        start_node, end_node = self.get_node(source), self.get_node(destination)

        # make djiikstra table
        pass




# Main function
if __name__ == "__main__":
    graph = Graph()
    df = pd.read_csv('node_data.csv')
    for i in range(len(df)):
        graph.add_node((df['X'][i], df['Y'][i]), df['Name'][i])
    
    for node in graph.nodes:
        count = random.randint(1, 5)

        for i in range(count):
            neighbor = random.choice(list(graph.nodes))
            distance = random.randint(1, 10)
            if neighbor != node:
                graph.add_edge(node, neighbor, distance)
    
    for node in graph.nodes:
        print(node.name, [[n.name, graph.distance[node][n]] for n in node.neighbors])

    

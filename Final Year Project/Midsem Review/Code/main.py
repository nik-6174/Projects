import pandas as pd
import random
from collections import defaultdict, deque
import heapq
import math

# create the graph node
class Node():
    def __init__(self, coordinates, name):
        self.coordinates = coordinates
        self.name = name
        self.neighbors = set()
        self.charge = False

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
        start_node, end_node = self.get_node[source], self.get_node[destination]

        # function to find manhattan distance between a node and the end node
        heuristic_distance_from_end = lambda coordinates: abs(coordinates[0] - end_node.coordinates[0]) + abs(coordinates[1] - end_node.coordinates[1])

        # coefficients for the heuristic function
        h1 = 1 # coefficient for the distance
        h2 = 0 # coefficient for the time
        h3 = 1 # coefficient for the heuristic distance from end point
        h4 = 1


        # find the shortest path
        visited = {}
        last_node = {}
        queue = [[0, 0, start_node, [start_node.name]]] # [heuristic value, distance, distance]
        count = 0

        while queue:
            count += 1
            heuristic, distance, node, path = heapq.heappop(queue)
            if node == end_node:
                print(f"The count is :{count}")
                return distance, path
            if node not in visited or visited[node] > heuristic:
                visited[node] = heuristic
                for neighbor in node.neighbors:
                    neighbor_heuristic = h1 * (distance + self.distance[node][neighbor]) + h2 * self.time[node][neighbor] + h3 * heuristic_distance_from_end(neighbor.coordinates)
                    heapq.heappush(queue, [neighbor_heuristic, distance + self.distance[node][neighbor], neighbor, path + [neighbor.name]])
        return float('inf'), None

        



# Main function
if __name__ == "__main__":
    graph = Graph()

    # Add 50 nodes to the graph
    num_nodes = 50
    node_names = [chr(65 + i) for i in range(num_nodes)]
    for name in node_names:
        x = random.uniform(0, 100)  # Random x-coordinate within the range 0-100
        y = random.uniform(0, 100)  # Random y-coordinate within the range 0-100
        graph.add_node((x, y), name)

    # Add edges to the graph
    num_edges = 100  # Target number of edges
    added_edges = set()  # Keep track of added edges to avoid duplicates
    while len(added_edges) < num_edges:
        node1, node2 = random.sample(graph.nodes, 2)  # Randomly select two nodes
        if (node1, node2) in added_edges or (node2, node1) in added_edges:
            continue  # Skip if the edge already exists or is a duplicate
        distance = math.sqrt((node1.coordinates[0] - node2.coordinates[0]) ** 2 +
                             (node1.coordinates[1] - node2.coordinates[1]) ** 2)
        graph.add_edge(node1, node2, int(distance) + random.randint(1, 10))
        added_edges.add((node1, node2))

    # Calculate the shortest path between two random nodes and print it
    start_node = random.choice(list(graph.nodes))
    end_node = random.choice(list(graph.nodes))
    shortest_path, path_names = graph.shortest_path(start_node.name, end_node.name)
    # Calculate the shortest path and print it
    print(path_names)

    print("Shortest path:", shortest_path)

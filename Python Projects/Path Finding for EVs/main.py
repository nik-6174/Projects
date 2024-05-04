import os
import pandas as pd
import heapq
from math import radians, sin, cos, sqrt, atan2
from collections import defaultdict
import bisect

# Define the file paths for nodes.csv, edges.csv, and charging.csv within the 'data' folder
nodes_file = os.path.join('data', 'nodes.csv')
edges_file = os.path.join('data', 'edges.csv')
charging_file = os.path.join('data', 'charging.csv')

# Load nodes.csv, edges.csv, and charging.csv into pandas DataFrames
nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file)
charging_df = pd.read_csv(charging_file)

# Define the Node class
class Node:
    def __init__(self, node_id, longitude, latitude, street_count, highway):
        self.id = node_id
        self.coordinates = (latitude, longitude)
        self.street_count = street_count
        self.highway = highway
        self.neighbors = set()
        self.charge = False  # By default, nodes are not charging stations

    def __lt__(self, other):
        return self.id < other.id

# Define the Graph class
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)

    def add_node(self, node_id, longitude, latitude, street_count, highway):
        node = Node(node_id, longitude, latitude, street_count, highway)
        self.nodes.add(node)
        return node

    def add_edge(self, node_id1, node_id2, distance):
        self.edges[node_id1][node_id2] = distance
        self.edges[node_id2][node_id1] = distance

    def add_charging_nodes(self, charging_df):
        charging_nodes = set(charging_df['node_id'])
        for node in self.nodes:
            if node.id in charging_nodes:
                node.charge = True

    def haversine_distance(self, coordinates1, coordinates2):
        # Calculate the distance between two coordinates using the Haversine formula
        lat1, lon1 = coordinates1
        lat2, lon2 = coordinates2
        R = 6371.0  # Radius of the Earth in kilometers
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    def build_graph(self, nodes_df, edges_df, charging_df):
        # Add nodes to the graph
        for idx, row in nodes_df.iterrows():
            node_id = row['node_id']
            longitude = row['longitude']
            latitude = row['latitude']
            street_count = row['street_count']
            highway = row['highway']
            node = self.add_node(node_id, longitude, latitude, street_count, highway)

        # Add charging information to nodes
        self.add_charging_nodes(charging_df)

        # Add edges to the graph
        for idx, row in edges_df.iterrows():
            node_id1 = row['node1']
            node_id2 = row['node2']
            coordinates1 = nodes_df[nodes_df['node_id'] == node_id1][['latitude', 'longitude']].values[0]
            coordinates2 = nodes_df[nodes_df['node_id'] == node_id2][['latitude', 'longitude']].values[0]
            distance = self.haversine_distance(coordinates1, coordinates2)
            self.add_edge(node_id1, node_id2, distance)

# Create an instance of the Graph class
graph = Graph()

# Build the graph using the provided dataframes
graph.build_graph(nodes_df, edges_df, charging_df)

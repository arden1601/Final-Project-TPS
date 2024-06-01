import configs.variables as var
import random

# Define node positions
p_node_positions = {
  1: (100, 100),
  2: (200, 200),
  3: (300, 300),
  4: (400, 400),
  5: (400, 300),
}

p_edge_list = [{
  'edge': (1, 2),
  'weight': 1,
  },{
  'edge': (2, 3),
  'weight': 1,
  },{
  'edge': (3, 4),
  'weight': 1,
}]

# Function to generate random vertices
def generate_random_vertices(num_vertices, x_range, y_range, existing_vertices):
  node_positions = existing_vertices.copy()
  start_index = max(node_positions.keys(), default=1)
  for i in range(start_index, start_index + num_vertices):
    node_positions[i] = (random.randint(0, x_range / var.minGap) * var.minGap, random.randint(0, y_range / var.minGap) * var.minGap)
  return node_positions

# Function to generate random edges
def generate_random_edges(num_edges, num_vertices, weight_range, existing_edges):
  edge_list = existing_edges.copy()
  while len(edge_list) < num_edges:
    v1 = random.randint(1, num_vertices)
    v2 = random.randint(1, num_vertices)
    if v1 != v2 and not any(edge['edge'] == (v1, v2) or edge['edge'] == (v2, v1) for edge in edge_list):
      edge_list.append({
        'edge': (v1, v2),
        'weight': random.randint(*weight_range)
      })
  return edge_list
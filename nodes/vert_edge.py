import configs.variables as var
import random

# Function to generate random vertices
def generate_random_vertices(num_vertices, x_range, y_range, existing_vertices):
  node_positions = existing_vertices.copy()
  start_index = max(node_positions.keys(), default=1)
  for i in range(start_index, start_index + num_vertices):
    node_positions[i] = (x_range[0] + random.randint(0, (x_range[1] - x_range[0]) / var.minGap) * var.minGap, y_range[0] + random.randint(0, (y_range[1] - y_range[0]) / var.minGap) * var.minGap)
  return node_positions

# Function to generate random edges
def generate_random_edges(num_edges, num_vertices, weight_range, existing_edges):
  edge_list = existing_edges.copy()
  while len(edge_list) < num_edges:
    v1 = random.randint(1, num_vertices)
    v2 = random.randint(1, num_vertices)

    v1_x, v1_y = var.node_positions[v1]
    v2_x, v2_y = var.node_positions[v2]
    
    while not (v1_x == v2_x or v1_y == v2_y):
      v1 = random.randint(1, num_vertices)
      v2 = random.randint(1, num_vertices)
      v1_x, v1_y = var.node_positions[v1]
      v2_x, v2_y = var.node_positions[v2]
    
    if v1 != v2 and not any(edge['edge'] == (v1, v2) or edge['edge'] == (v2, v1) for edge in edge_list):
      edge_list.append({
        'edge': (v1, v2),
        'weight': random.randint(*weight_range)
      })
  return edge_list
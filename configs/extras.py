import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target, width):
  # Find G with the width
  for G in var.G:
    if G['width'] >= width:
      return nx.dijkstra_path(G['graph'], source, target)

def generate_width_required(type):
  if type == 'bike':
    return 1
  elif type == 'car':
    return 2

def recount_quota():
  # Loop for each edge
  for edge in var.G[0]['graph'].edges():
    # Get the edge position
    position = edge[0]
    next_target = edge[1]
    
    # Get the current value of the edge
    current_value = var.G[0]['graph'][position][next_target]['weight']
    
    # Find how many vehicles that are also in the same position and target
    same_target = [v for v in var.vehicles if v.position == position and v.next_target == next_target]
    total = len(same_target)
      
    # Print the current position quota
    max = var.getEdgeLength(position, next_target)
    quota = (max - total) / max
    
    if quota <= 0 and current_value < var.gigaNumber:
      # Add the weight of the graph by giganumber
      var.G[0]['graph'][position][next_target]['weight'] += var.gigaNumber
      
    elif current_value > var.gigaNumber:
      # Reduce the weight of the graph by giganumber
      var.G[0]['graph'][position][next_target]['weight'] -= var.gigaNumber
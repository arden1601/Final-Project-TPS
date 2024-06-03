import configs.variables as var
import networkx as nx

def generate_shortest_path(source, target, width):
  # Find G with the width
  for G in var.G:
    if G['width'] >= width:
      return nx.dijkstra_path(G['graph'], source, target)

def generate_width_required(type):
  # Iterate over the veh_choices
  for veh in var.veh_choices:
    if veh['name'] == type:
      return veh['width']

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
      
def check_nodes_contain_vehicle():
  # Loop for each nodes
  for node, pos in var.node_positions.items():
    pos_new = (pos[0] + var.viewMargin[0], pos[1] + var.viewMargin[1])
    
    x1, y1 = pos_new[0] - var.edgeWidth*1.4, pos_new[1] - var.edgeWidth*1.4
    x2, y2 = pos_new[0] + var.edgeWidth*1.4, pos_new[1] + var.edgeWidth*1.4
    
    # Definition to draw circle in the node
    gonnaAppend = False
    
    # Check if the node contains a vehicle
    save_veh = None
    for veh in var.vehicles:
      # check if the vehicle exists in node_occupy
      if any([node_occupy['vehicle'] == veh for node_occupy in var.node_occupy]):
        continue
      
      x, y = veh.x + var.viewMargin[0], veh.y + var.viewMargin[1]
      x_most, y_most = x + veh.width, y + veh.height
      
      if (x >= x1 and x <= x2) and (y >= y1 and y <= y2):
        gonnaAppend = True
        save_veh = veh
        break
      elif (x_most >= x1 and x_most <= x2) and (y_most >= y1 and y_most <= y2):
        gonnaAppend = True
        save_veh = veh
        break
      elif (x >= x1 and x <= x2) and (y_most >= y1 and y_most <= y2):
        gonnaAppend = True
        save_veh = veh
        break
      elif (x_most >= x1 and x_most <= x2) and (y >= y1 and y <= y2):
        gonnaAppend = True
        save_veh = veh
        break
      
    if gonnaAppend:
      var.node_occupy.append({
        'node': node,
        'vehicle': save_veh,
      })
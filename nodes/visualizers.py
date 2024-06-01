import configs.variables as var
import networkx as nx

def create_graph():
  G = nx.Graph()
  for edge in var.edge_list:
    G.add_edge(*edge['edge'], weight=edge['weight'])
  var.G = G

def draw_graph():
  color = var.colors
  win = var.win
  win.fill(color['WHITE'])
  
  # Draw edges
  node_positions = var.node_positions
  
  for edge in var.G.edges():
    # Get start and end positions
    start_pos = node_positions[edge[0]]
    end_pos = node_positions[edge[1]]
    
    # color_used = color['RED'] if edge in zip(shortest_path, shortest_path[1:]) or edge[::-1] in zip(shortest_path, shortest_path[1:]) else color['BLACK']
    
    # Draw edge line
    var.pyptr.draw.line(win, color['BLACK'], start_pos, end_pos, var.edgeWidth)
  
  # Draw nodes
  for node, pos in node_positions.items():
    # Draw node circle
    var.pyptr.draw.circle(win, color['BLUE'], pos, var.edgeWidth)
    
    # Draw node number
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(node), True, color['WHITE'])
    
    win.blit(text, (pos[0] - 5, pos[1] - 8)) # -5 and -8 are offsets to center the text
    
def draw_vehicles():
  pass
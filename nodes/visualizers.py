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
    
  # Draw weights
  for edge in var.G.edges():
    # Get start and end positions
    start_pos = node_positions[edge[0]]
    end_pos = node_positions[edge[1]]
    
    # Get weight
    weight = var.G[edge[0]][edge[1]]['weight']
    
    # Draw weight
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(weight), True, color['BLACK'])
    
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(weight), True, color['BLACK'])
    
    x, y = 0, 0
    # check if the edge horizontal or vertical
    gap = var.edgeWidth * 1.2
    if start_pos[0] == end_pos[0]:
      # vertical
      x = start_pos[0] - gap
      y = (start_pos[1] + end_pos[1]) // 2
    else:
      # horizontal
      x = (start_pos[0] + end_pos[0]) // 2
      y = start_pos[1] - gap
    
    win.blit(text, (x, y))
    
def draw_vehicles():
  # Move and draw vehicles
  for vehicleHere in var.vehicles:
    vehicleHere.goToTarget()
    vehicleHere.draw(var.win)

def draw_the_road():
  road_size = var.edgeWidth
  for i in var.edge_list:
    x = var.node_positions[i['edge'][0]][0]
    y = var.node_positions[i['edge'][0]][1]
    _x = var.node_positions[i['edge'][1]][0]
    _y = var.node_positions[i['edge'][1]][1]
    scale_w = 1 if abs(x - _x) / road_size == 0 else abs(x - _x) / road_size
    scale_h = 1 if abs(y - _y) / road_size == 0 else abs(y - _y) / road_size
    var.pyptr.draw.rect(var.win, var.colors['GRAY'], var.pyptr.Rect(x-15, y-15, road_size*scale_w, road_size*scale_h))
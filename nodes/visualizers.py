import configs.variables as var
import networkx as nx

def create_graph():
  unique_widths = {edge['width'] for edge in var.edge_list}
  for widths in unique_widths:
    G = nx.DiGraph()
    for edge in var.edge_list:
      if edge['width'] >= widths:
        G.add_edge(*edge['edge'], weight=edge['weight'])
    
    var.G.append({
      'graph': G,
      'width': widths
    })

def draw_graph():
  color = var.colors
  win = var.win
  win.fill(color['WHITE'])
  
  # Draw edges
  node_positions = var.node_positions
  
  usedG = var.G[0]['graph']
  for idx, edge in enumerate(usedG.edges()):
    # Get start and end positions
    start_pos = node_positions[edge[0]]
    end_pos = node_positions[edge[1]]
    
    # Check the edge width
    width = var.edge_list[idx]['width']
    
    # check if the direction is up or down
    gap = var.gap
    x, y = 0, 0
    colorUsed = color['BLACK']
    if start_pos[0] == end_pos[0]:
      # vertical
      if start_pos[1] < end_pos[1]: # the road is a vector to the bottom
        x += gap
      else: # the road is a vector to the top
        x -= gap
        colorUsed = color['GRAY']
        
    else:
      # horizontal
      if start_pos[0] < end_pos[0]: # the road is a vector to the right
        y -= gap
      else: # the road is a vector to the left
        y += gap
        colorUsed = color['GRAY']
    
    # Add start and end positions with x and y
    start_pos = (start_pos[0] + x + var.viewMargin[0], start_pos[1] + y + var.viewMargin[1])
    end_pos = (end_pos[0] + x + var.viewMargin[1], end_pos[1] + y + var.viewMargin[1])
    
    # Draw edge line
    var.pyptr.draw.line(win, colorUsed, start_pos, end_pos, var.edgeWidth)
  
  # Draw nodes
  for node, pos in node_positions.items():
    # Draw node circle
    pos_new = (pos[0] + var.viewMargin[0], pos[1] + var.viewMargin[1])
    var.pyptr.draw.circle(win, color['BLUE'], pos_new, var.edgeWidth*1.4)
    
    # Draw node number
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(node), True, color['WHITE'])
    
    win.blit(text, (pos[0] - 5 + var.viewMargin[0], pos[1] - 8 + var.viewMargin[1])) # -5 and -8 are offsets to center the text
    
  # Draw weights
  for edge in usedG.edges():
    # Get start and end positions
    start_pos = node_positions[edge[0]]
    end_pos = node_positions[edge[1]]
    
    # Get weight
    weight = usedG[edge[0]][edge[1]]['weight']
    
    # Draw weight
    font = var.pyptr.font.Font(None, 24)
    
    x, y = 0, 0
    # check if the edge horizontal or vertical
    gap = var.gap * 1.2
    if start_pos[0] == end_pos[0]:
      # moving horizontal
      x = start_pos[0] - gap
      y = (start_pos[1] + end_pos[1]) // 2
      
      if start_pos[1] < end_pos[1]: # the road is a vector to the bottom
        # make the road moves to the right
        x += 2*gap + var.edgeWidth
      else: # the road is a vector to the top
        # make the road moves to the left
        x -= gap
        
    else:
      # moving vertical
      x = (start_pos[0] + end_pos[0]) // 2
      y = start_pos[1] - gap
      
      if start_pos[0] < end_pos[0]: # the road is a vector to the right
        # make the road moves to the bottom
        y -= gap
      else: # the road is a vector to the left
        # make the road moves to the top
        y += 2*gap + var.edgeWidth
        
    # Get how many vehicles that are also in the same position and target
    same_target = [v for v in var.vehicles if v.position == edge[0] and v.next_target == edge[1]]
    total = len(same_target)
    # Count quota
    max = var.getEdgeLength(edge[0], edge[1])
    quota = (max - total) / max
    
    toRender = quota if var.show == 'quota' else weight if var.show == 'weight' else total if var.show == 'vehicles' else 0
    text = font.render(str(toRender), True, color['BLACK'])
    
    win.blit(text, (x + var.viewMargin[0], y + var.viewMargin[1]))
    
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
    var.pyptr.draw.rect(var.win, var.colors['GRAY'], var.pyptr.Rect(x-15 + var.viewMargin[0], y-15 + var.viewMargin[1], road_size*scale_w, road_size*scale_h))
      
def visualizeEverything():
  draw_graph()	
  # draw_the_road()
  draw_vehicles()
  draw_vehicles()
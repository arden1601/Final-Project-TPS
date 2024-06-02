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

def draw_edges():
  usedG = var.G[0]['graph']
  for edge in usedG.edges():
    # Get start and end positions
    start_pos = var.node_positions[edge[0]]
    end_pos = var.node_positions[edge[1]]
    
    # check if the direction is up or down
    gap = var.gap
    x, y = 0, 0
    colorUsed = var.colors['BLACK']
    if start_pos[0] == end_pos[0]:
      # vertical
      if start_pos[1] < end_pos[1]: # the road is a vector to the bottom
        x += gap
      else: # the road is a vector to the top
        x -= gap
        colorUsed = var.colors['GRAY']
        
    else:
      # horizontal
      if start_pos[0] < end_pos[0]: # the road is a vector to the right
        y -= gap
      else: # the road is a vector to the left
        y += gap
        colorUsed = var.colors['GRAY']
    
    # Add start and end positions with x and y
    start_pos = (start_pos[0] + x + var.viewMargin[0], start_pos[1] + y + var.viewMargin[1])
    end_pos = (end_pos[0] + x + var.viewMargin[1], end_pos[1] + y + var.viewMargin[1])
    
    # Draw edge line
    var.pyptr.draw.line(var.win, colorUsed, start_pos, end_pos, var.edgeWidth)

def draw_nodes():
  for node, pos in var.node_positions.items():
    # Draw node circle
    pos_new = (pos[0] + var.viewMargin[0], pos[1] + var.viewMargin[1])
    var.pyptr.draw.circle(var.win, var.colors['BLUE'], pos_new, var.edgeWidth*1.4)
    
    # Draw a square surrounding the circle
    var.pyptr.draw.rect(
      var.win,
      var.colors['BLACK'],
      var.pyptr.Rect(
        pos_new[0] - var.edgeWidth*1.4,
        pos_new[1] - var.edgeWidth*1.4,
        var.edgeWidth*2.8,
        var.edgeWidth*2.8),
      2)
    
    # Draw node number
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(node), True, var.colors['WHITE'])
    
    var.win.blit(text, (pos[0] - 5 + var.viewMargin[0], pos[1] - 8 + var.viewMargin[1])) # -5 and -8 are offsets to center the text

def draw_weights():
  usedG = var.G[0]['graph']
  for edge in usedG.edges():
    # Get start and end positions
    start_pos = var.node_positions[edge[0]]
    end_pos = var.node_positions[edge[1]]
    
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
    text = font.render(str(toRender), True, var.colors['BLACK'])
    
    var.win.blit(text, (x + var.viewMargin[0], y + var.viewMargin[1]))
    
def draw_vehicles():
  # Move and draw vehicles
  for vehicleHere in var.vehicles:
    vehicleHere.goToTarget()
    vehicleHere.draw(var.win)

def draw_the_road():
  strip = var.pyptr.image.load('./assets/yellow_strip.jpg')
  strip_vertical = var.pyptr.transform.scale(strip, (25, 25))
  strip_horizontal = var.pyptr.transform.rotate(strip_vertical, 90)
  road_size = var.edgeWidth + 20
  for i in var.edge_list:
    x  = var.var.node_positions[i['edge'][0]][0]
    y  = var.var.node_positions[i['edge'][0]][1]
    _x = var.var.node_positions[i['edge'][1]][0]
    _y = var.var.node_positions[i['edge'][1]][1]
    scale_w = 1 if abs(x - _x) / road_size == 0 else abs(x - _x) / road_size
    scale_h = 1 if abs(y - _y) / road_size == 0 else abs(y - _y) / road_size
    var.pyptr.draw.rect(var.win, var.colors['GRAY'], var.pyptr.Rect(x - 25 + var.viewMargin[0], y - 30 + var.viewMargin[1], road_size*scale_w + 20, road_size*scale_h + 20))
  # Draw strip Horizontal
  for i in range(0, 1200,50):
    var.win.blit(strip_horizontal, (i + 40, 137))
    var.win.blit(strip_horizontal, (i + 40, 337))
    if i < 500:
      var.win.blit(strip_horizontal, (i + 40, 537))
    if i > 100:
      var.win.blit(strip_horizontal, (i + 40, 737))
  for i in range(0, 800,50):
    if i > 75 and i < 750:
      var.win.blit(strip_vertical, (142, i + 40))
    if i < 200:
      var.win.blit(strip_vertical, (242, i + 40))
    if i > 500:
      var.win.blit(strip_vertical, (342, i + 40))
    var.win.blit(strip_vertical, (1042, i + 40))


def draw_clock():
  font = var.pyptr.font.Font(None, 24)
  # create an xx:xx format
  clock_hour = str(var.clock)
  clock_min = str(var.clock_min)
  clock = str(0 if var.clock < 10 else '') + clock_hour + ':' + str(0 if var.clock_min < 10 else '') + clock_min
  
  text = font.render(str(clock), True, var.colors['BLACK'])
  var.win.blit(text, (var.width - var.viewMargin[0]*2, var.viewMargin[1]))

def draw_busy():
  for node in var.busy_node:
    pos = var.node_positions[node]
    pos_new = (pos[0] + var.viewMargin[0], pos[1] + var.viewMargin[1])
    
    x1, y1 = pos_new[0] - var.edgeWidth*1.4, pos_new[1] - var.edgeWidth*1.4
    
    var.pyptr.draw.ellipse(var.win, var.colors['RED'], var.pyptr.Rect(x1, y1, var.edgeWidth*2.8, var.edgeWidth*2.8), 2)

def visualizeEverything():
  var.win.fill(var.colors['WHITE'])
  draw_edges()
  draw_nodes()
  draw_weights()
  draw_busy()
  # draw_the_road()
  draw_vehicles()
  draw_clock()
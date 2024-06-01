import configs.variables as var
import nodes.positions as positions
import networkx as nx

def create_graph():
	var.G = nx.Graph()
	G = var.G
	G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

def draw_graph():
  color = var.colors
  win = var.win
  win.fill(color['WHITE'])
  
  # Draw edges
  node_positions = positions.node_positions
  print(node_positions)
  for edge in var.G.edges():
    start_pos = node_positions[edge[0]]
    end_pos = node_positions[edge[1]]
    var.pyptr.draw.line(win, color['BLACK'], start_pos, end_pos, 2)
  
  # Draw nodes
  for node, pos in node_positions.items():
    var.pyptr.draw.circle(win, color['BLUE'], pos, 20)
    font = var.pyptr.font.Font(None, 24)
    text = font.render(str(node), True, color['WHITE'])
    win.blit(text, (pos[0] - 5, pos[1] - 8))
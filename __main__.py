# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import nodes.vert_edge as vert_edge
# import nodes.simulation_map as sm

road_size = 25
gray = (119, 119, 119)

def draw_road(x, y, scale_w = 1, scale_h = 1):
	# print(x, y, road_size*scale_w, road_size*scale_h)
	var.pyptr.draw.rect(var.win, gray, pygame.Rect(x-15, y-15, road_size*scale_w, road_size*scale_h))

def main(): 
	# Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 1000, 600
	screen.init_screen() 
	
	# Initialize Nodes and Edges
  	# Parameters
	total_vertices = 30
	total_edges = 40
	y_range = 500
	weight_range = (1, 10)

	# Generate random vertices and edges
	var.node_positions = {
		1: (0, 100),
		2: (100, 0),
		3: (100, 100),
		4: (100, 400),
		5: (200, 400),
		6: (200, 600),
		7: (600, 100),
		8: (600, 600),
		}
	var.edge_list = [{
		'edge': (1, 3),
		'weight': 1,
		},{
		'edge': (2, 3),
		'weight': 1,
		},{
		'edge': (3, 4),
		'weight': 1,
		},{
		'edge': (4, 5),
		'weight': 1,
		},{
		'edge': (5, 6),
		'weight': 1,
		},{
		'edge': (3, 7),
		'weight': 1,
		},{
		'edge': (7, 8),
		'weight': 1,
		}
  ]
     
	# Create Graph
	visualizers.create_graph()

	# Main loop
	running = True
	while running:
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				running = False

		visualizers.draw_graph()
  
		for i in var.edge_list:
			x = var.node_positions[i['edge'][0]][0]
			y = var.node_positions[i['edge'][0]][1]
			_x = var.node_positions[i['edge'][1]][0]
			_y = var.node_positions[i['edge'][1]][1]
			scale_w = 1 if abs(x - _x) / road_size == 0 else abs(x - _x) / road_size
			scale_h = 1 if abs(y - _y) / road_size == 0 else abs(y - _y) / road_size
			draw_road(x,y, scale_w, scale_h)
   
		var.pyptr.display.flip()
  
	var.pyptr.quit()

if __name__ == "__main__":
  main()
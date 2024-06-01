# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import nodes.vert_edge as vert_edge
import math
# import nodes.simulation_map as sm
import networkx as nx

road_size = 25
gray = (119, 119, 119)

def draw_road(x, y, scale_w = 1, scale_h = 1):
	# print(x, y, road_size*scale_w, road_size*scale_h)
	var.pyptr.draw.rect(var.win, gray, pygame.Rect(x-15, y-15, road_size*scale_w, road_size*scale_h))

def move_along_path(path, positions, speed=1):
    # Initialize car position at the start of the path
    car_pos = list(positions[path[0]])
    current_index = 0

    while current_index < len(path) - 1:
        start_node = path[current_index]
        end_node = path[current_index + 1]
        start_pos = positions[start_node]
        end_pos = positions[end_node]

        dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        steps = int(distance / speed)
        step_dx, step_dy = dx / steps, dy / steps

        for _ in range(steps):
            car_pos[0] += step_dx
            car_pos[1] += step_dy
            yield car_pos

        current_index += 1

def shortest_path(source, target):
  var.shortest_path = nx.dijkstra_path(var.G, source, target)

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
		9: (1000, 100),
		10: (600, 0),
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
		},{
		'edge': (7, 9),
		'weight': 1,
		},{
		'edge': (7, 10),
		'weight': 1,
		}
  ]
     
	# Create Graph
	visualizers.create_graph()

	# Main loop
	shortest_path(1, 8)
	car_animation = move_along_path(var.shortest_path, var.node_positions, speed=.5)
	running = True
	while running:
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				running = False

		visualizers.draw_graph()	
		print()
  
		try:
			car_pos = next(car_animation)
			var.pyptr.draw.circle(var.win, var.colors['RED'], (int(car_pos[0]), int(car_pos[1])), 10)
		except StopIteration:
			pass
   
		# for i in var.edge_list:
		# 	x = var.node_positions[i['edge'][0]][0]
		# 	y = var.node_positions[i['edge'][0]][1]
		# 	_x = var.node_positions[i['edge'][1]][0]
		# 	_y = var.node_positions[i['edge'][1]][1]
		# 	scale_w = 1 if abs(x - _x) / road_size == 0 else abs(x - _x) / road_size
		# 	scale_h = 1 if abs(y - _y) / road_size == 0 else abs(y - _y) / road_size
		# 	draw_road(x,y, scale_w, scale_h)
  
		var.pyptr.display.flip()
		visualizers.draw_vehicles()
  
	var.pyptr.quit()

if __name__ == "__main__":
  main()
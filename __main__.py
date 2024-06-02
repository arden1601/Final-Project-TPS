# import packages
import pygame
import configs.variables as var
import configs.screen as screen
import nodes.visualizers as visualizers
import object.vehicle as vehicle
import random

def main(): 
	# Initialize Pygame
	var.pyptr = pygame
	var.pyptr.init()
 
	# Initialize Screen
	var.width, var.height = 1000, 600
	screen.init_screen() 

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
		},{
		'edge': (6, 8),
		'weight': 1,
		}
  ]
     
	# Create Graph
	visualizers.create_graph()

	# Main loop
	initCars = [1, 2, 3, 4, 5, 7, 6, 9, 10]
	var.vehicles = []
 	# Create vehicles with initial positions
	for i in initCars:
		# random the color
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		var.vehicles.append(vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, i, 8))
 
	running = True
	while running:
		for event in var.pyptr.event.get():
			if event.type == var.pyptr.QUIT:
				running = False

		visualizers.draw_graph()	
		# visualizers.draw_the_road()
		visualizers.draw_vehicles()
  
		visualizers.draw_vehicles()
		var.pyptr.display.flip()
  
	var.pyptr.quit()

if __name__ == "__main__":
  main()
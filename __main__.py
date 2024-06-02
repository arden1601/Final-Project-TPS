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
	var.width, var.height = 1200, 800
	screen.init_screen() 
	
	var.node_positions = {
		1: (0, 100),
		2: (100, 0),
		3: (100, 100),
		4: (100, 400),
		5: (200, 400),
		6: (200, 600),
		7: (600, 100),
		8: (600, 600),
		9: (700, 400),
		10: (800, 600),
		11: (900, 100),
		12: (900, 600),
		13: (800, 400),
  	14: (700, 600),
		}
	var.edge_list = [{
		'edge': (1, 3),
		'weight': 1,
		'width': 1
		},{
		'edge': (2, 3),
		'weight': 1,
		'width': 1
		},{
		'edge': (3, 4),
		'weight': 1,
  	'width': 1
		},{
		'edge': (4, 5),
		'weight': 1,
  	'width': 1
		},{
		'edge': (5, 6),
		'weight': 1,
  	'width': 1
		},{
		'edge': (3, 7),
		'weight': 10,
  	'width': 1
		},{
		'edge': (8, 7),
		'weight': 1,
  	'width': 1
		},{
		'edge': (6, 8),
		'weight': 1,
  	'width': 1
		},{
		'edge': (7, 11),
		'weight': 1,
  	'width': 1
		},{
		'edge': (11, 12),
		'weight': 1,
  	'width': 1
		},{
		'edge': (12, 10),
		'weight': 1,
  	'width': 1
		},{
		'edge': (7, 8),
		'weight': 1,
  	'width': 1
		},{
		'edge': (10, 12),
		'weight': 1,
  	'width': 1
		},{
		'edge': (11, 7),
		'weight': 1,
  	'width': 1
		},{
		'edge': (10, 13),
		'weight': 1,
  	'width': 1
		},{
		'edge': (13, 9),
		'weight': 1,
  	'width': 1
		},{
		'edge': (9, 14),
		'weight': 1,
  	'width': 1
		}
  ]
 
	# Remove edges that have nodes that are not in the node_positions
	currentLen = len(var.edge_list)
	var.edge_list = [edge for edge in var.edge_list if edge['edge'][0] in var.node_positions and edge['edge'][1] in var.node_positions]
 
	# Show warning when there are edges that are not in the node_positions
	if currentLen != len(var.edge_list):
		print('WARNING: Some edges are not in the node_positions')
	else:
		print('All edges are in the node_positions')
	
	# Create Graph
	visualizers.create_graph()

	# Main loop
	initVehicle = [
   {
		'begin': 1,
		'end': 14,
		'type': 'bike'
	 }]
	# },
	# {
	# 	'begin': 1,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 1,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
 	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# },
	# {
	# 	'begin': 2,
	# 	'end': 8,
	# 	'type': 'bike'
	# }]
 
	var.vehicles = []
 	# Create vehicles with initial positions
	for veh in initVehicle:
		# random the color
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		newVeh = vehicle.Vehicle((var.edgeWidth, var.edgeWidth), color, veh['begin'], veh['end'])
		if not newVeh.next_target == newVeh.position:
			var.vehicles.append(newVeh)
   
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

if __name__ == "__main__":
  main()